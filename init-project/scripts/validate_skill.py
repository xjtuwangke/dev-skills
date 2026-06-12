#!/usr/bin/env python3
"""Validate init-project scripts against representative project fixtures."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DETECTOR = SCRIPT_DIR / "detect_project.py"
RENDERER = SCRIPT_DIR / "render_agents_docs.py"
MAVEN_INSPECTOR = SCRIPT_DIR / "templates" / "maven-java" / "inspect_maven_project.py"
DEPS_TREE = SCRIPT_DIR / "templates" / "maven-java" / "generate_dependency_tree.py"
SPRING_INSPECTOR = SCRIPT_DIR / "templates" / "springboot3-webflux" / "inspect_springboot_webflux.py"
KARATE_INSPECTOR = SCRIPT_DIR / "templates" / "karate-at" / "inspect_karate_project.py"
BUSINESS_FIXTURE = ROOT / "evals" / "fixtures" / "springboot-commerce-webflux"


def run(command: list[str], cwd: Path | None = None, allow_fail: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0 and not allow_fail:
        raise AssertionError(
            f"Command failed: {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def run_json(command: list[str], allow_fail: bool = False) -> dict:
    result = run(command, allow_fail=allow_fail)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"Invalid JSON from {' '.join(command)}: {exc}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        ) from exc


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_webflux(root: Path) -> Path:
    project = root / "webflux"
    write(
        project / "pom.xml",
        """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <parent><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-parent</artifactId><version>3.3.2</version></parent>
  <groupId>com.example</groupId><artifactId>payments</artifactId><version>1.0.0</version>
  <properties><java.version>21</java.version></properties>
  <dependencies><dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-webflux</artifactId></dependency></dependencies>
</project>
""",
    )
    write(
        project / "src/main/java/com/example/payments/PaymentApplication.java",
        "package com.example.payments; import org.springframework.boot.autoconfigure.SpringBootApplication; @SpringBootApplication class PaymentApplication {}\n",
    )
    write(
        project / "src/main/java/com/example/payments/PaymentController.java",
        "package com.example.payments; import org.springframework.web.bind.annotation.RestController; import reactor.core.publisher.Mono; @RestController class PaymentController { Mono<String> health(){ return Mono.just(\"ok\"); } }\n",
    )
    write(
        project / "src/main/java/com/example/payments/PaymentClient.java",
        "package com.example.payments; import org.springframework.web.reactive.function.client.WebClient; class PaymentClient { WebClient client; }\n",
    )
    write(
        project / "src/test/java/com/example/payments/PaymentControllerTest.java",
        "package com.example.payments; import org.springframework.test.web.reactive.server.WebTestClient; class PaymentControllerTest { WebTestClient client; }\n",
    )
    write(project / "src/main/resources/application.yml", "server: { port: 8080 }\n")
    return project


def make_karate(root: Path) -> Path:
    project = root / "karate"
    write(
        project / "pom.xml",
        """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId><artifactId>api-at</artifactId><version>1.0.0</version>
  <dependencies><dependency><groupId>com.intuit.karate</groupId><artifactId>karate-junit5</artifactId><version>1.4.1</version></dependency></dependencies>
</project>
""",
    )
    write(
        project / "src/test/java/com/example/features/payments.feature",
        "@smoke @payments\nFeature: payments\n  Scenario: create payment\n    * match 1 == 1\n",
    )
    write(
        project / "src/test/java/com/example/runners/PaymentsRunner.java",
        "package com.example.runners; import com.intuit.karate.junit5.Karate; class PaymentsRunner { @Karate.Test Karate run(){ return Karate.run(\"classpath:com/example/features\"); } }\n",
    )
    write(project / "karate-config.js", "function fn() { var env = karate.env || 'dev'; if (env == 'qa') return {}; return {}; }\n")
    write(project / "src/test/resources/payloads/create-payment.json", "{\"amount\":10}\n")
    return project


def make_multimodule(root: Path) -> tuple[Path, Path]:
    project = root / "multi"
    write(
        project / "pom.xml",
        """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId><artifactId>root</artifactId><version>1.0.0</version>
  <packaging>pom</packaging>
  <properties><java.version>17</java.version></properties>
  <modules><module>service</module></modules>
  <dependencyManagement><dependencies><dependency><groupId>org.junit.jupiter</groupId><artifactId>junit-jupiter-api</artifactId><version>5.10.0</version><scope>test</scope></dependency></dependencies></dependencyManagement>
</project>
""",
    )
    write(
        project / "service/pom.xml",
        """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <parent><groupId>com.example</groupId><artifactId>root</artifactId><version>1.0.0</version></parent>
  <artifactId>service</artifactId>
  <dependencies><dependency><groupId>org.junit.jupiter</groupId><artifactId>junit-jupiter-api</artifactId><scope>test</scope><exclusions><exclusion><groupId>org.opentest4j</groupId><artifactId>opentest4j</artifactId></exclusion></exclusions></dependency></dependencies>
</project>
""",
    )
    fake_bin = root / "bin"
    fake_mvn = fake_bin / "fake-mvn"
    write(
        fake_mvn,
        """#!/usr/bin/env sh
for arg in "$@"; do
  case "$arg" in
    -DoutputFile=*) output="${arg#-DoutputFile=}" ;;
  esac
done
mkdir -p "$(dirname "$output")"
cat > "$output" <<'JSON'
{"groupId":"com.example","artifactId":"demo","version":"1.0.0","type":"jar","scope":"","classifier":"","optional":"false","children":[{"groupId":"org.junit.jupiter","artifactId":"junit-jupiter-api","version":"5.10.0","type":"jar","scope":"test","classifier":"","optional":"false","children":[]}]}
JSON
exit 0
""",
    )
    fake_mvn.chmod(0o755)
    return project, fake_mvn


def validate_webflux(project: Path) -> None:
    detection = run_json([sys.executable, str(DETECTOR), str(project)])
    assert detection["matched_templates"] == ["baseline", "maven-java", "springboot3-webflux"]
    spring = run_json([sys.executable, str(SPRING_INSPECTOR), str(project)])
    assert any("PaymentApplication.java" in item for item in spring["application_classes"])
    assert any("PaymentController.java" in item for item in spring["controllers_or_handlers"])

    render = run_json([sys.executable, str(RENDERER), str(project)])
    assert render["matched_templates"] == ["baseline", "maven-java", "springboot3-webflux"]
    architecture = (project / "agents/ARCHITECTURE_NOTES.md").read_text(encoding="utf-8")
    profile = (project / "agents/PROJECT_PROFILE.md").read_text(encoding="utf-8")
    assert "PaymentApplication.java" in architecture
    assert "PaymentController.java" in architecture
    assert "PaymentClient.java" in architecture
    assert "PaymentControllerTest.java" in architecture
    assert "Representative Feature Files\n- None detected" in architecture
    assert "com.example.payments" in profile
    assert "## Karate Evidence" not in profile
    assert '"karate-at": []' not in profile


def validate_karate(project: Path) -> None:
    detection = run_json([sys.executable, str(DETECTOR), str(project)])
    assert detection["matched_templates"] == ["baseline", "maven-java", "karate-at"]
    karate = run_json([sys.executable, str(KARATE_INSPECTOR), str(project)])
    assert "@smoke" in karate["tags"]
    assert any("PaymentsRunner.java" in item for item in karate["runner_classes"])

    render = run_json([sys.executable, str(RENDERER), str(project)])
    assert render["matched_templates"] == ["baseline", "maven-java", "karate-at"]
    architecture = (project / "agents/ARCHITECTURE_NOTES.md").read_text(encoding="utf-8")
    build = (project / "agents/BUILD_AND_TEST.md").read_text(encoding="utf-8")
    assert "@payments" in architecture
    assert "PaymentsRunner.java" in architecture
    assert "create-payment.json" in architecture
    assert "@smoke" in build
    assert "`dev`" in build
    assert "mvn test -Dtest=PaymentsRunner" in build
    profile = (project / "agents/PROJECT_PROFILE.md").read_text(encoding="utf-8")
    assert "## Spring Boot WebFlux Evidence" not in profile
    assert '"springboot3-webflux": []' not in profile


def validate_maven(project: Path, fake_mvn: Path) -> None:
    info = run_json([sys.executable, str(MAVEN_INSPECTOR), str(project)])
    assert info["is_maven_project"] is True
    assert info["pom_tree"]["modules"] == ["service"]
    assert info["pom_tree"]["module_details"][0]["coordinates"]["artifactId"] == "service"
    assert info["pom_tree"]["module_details"][0]["dependencies"][0]["exclusions"][0]["artifactId"] == "opentest4j"

    tree = run_json([sys.executable, str(DEPS_TREE), str(project), "--maven", str(fake_mvn)])
    assert tree["ok"] is True
    assert [run["module"] for run in tree["runs"]] == [None, "service"]
    assert tree["runs"][0]["tree"]["children"][0]["artifactId"] == "junit-jupiter-api"


def validate_explicit_template(root: Path) -> None:
    project = root / "explicit"
    write(
        project / "pom.xml",
        """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId><artifactId>explicit-demo</artifactId><version>1.0.0</version>
  <properties><java.version>17</java.version></properties>
</project>
""",
    )
    write(project / "src/main/java/com/example/App.java", "package com.example; class App {}\n")
    render = run_json(
        [
            sys.executable,
            str(RENDERER),
            str(project),
            "--template",
            "maven-java,springboot3-webflux",
        ]
    )
    assert render["matched_templates"] == ["baseline", "maven-java", "springboot3-webflux"]
    bad = run_json(
        [sys.executable, str(RENDERER), str(project), "--template", "nope"],
        allow_fail=True,
    )
    assert "Unsupported template" in bad["error"]


def validate_business_fixture() -> None:
    assert BUSINESS_FIXTURE.exists(), "business fixture is missing"
    assert (BUSINESS_FIXTURE / "pom.xml").exists()
    assert (BUSINESS_FIXTURE / "mvnw").exists()
    assert (BUSINESS_FIXTURE / "src/main/resources/openapi.yaml").exists()

    source_root = BUSINESS_FIXTURE / "src/main/java/com/acme/commerce"
    for folder in ["config", "model", "database", "service", "endpoint", "client", "pubsub"]:
        assert (source_root / folder).is_dir(), f"missing source folder: {folder}"

    env_files = sorted(path.name for path in (BUSINESS_FIXTURE / "src/main/resources").glob("application-*.yml"))
    assert env_files == [
        "application-dev.yml",
        "application-ppd.yml",
        "application-prd.yml",
        "application-sit.yml",
        "application-uat.yml",
    ]

    endpoint_count = 0
    for path in (source_root / "endpoint").glob("*.java"):
        text = path.read_text(encoding="utf-8")
        endpoint_count += sum(
            marker in line
            for line in text.splitlines()
            for marker in ["@GetMapping", "@PostMapping", "@PatchMapping", "@PutMapping", "@DeleteMapping"]
        )
    assert endpoint_count >= 20, f"expected at least 20 endpoint methods, got {endpoint_count}"

    openapi = (BUSINESS_FIXTURE / "src/main/resources/openapi.yaml").read_text(encoding="utf-8")
    assert openapi.count("\n  /api/") >= 20

    expected_docs = [
        "expected/AGENTS.md",
        "expected/AGENTS.zh.md",
        "expected/agents/PROJECT_PROFILE.md",
        "expected/agents/PROJECT_PROFILE.zh.md",
        "expected/agents/BUILD_AND_TEST.md",
        "expected/agents/BUILD_AND_TEST.zh.md",
        "expected/agents/BACKEND_SURFACES.md",
        "expected/agents/BACKEND_SURFACES.zh.md",
        "expected/agents/CALL_CHAINS.md",
        "expected/agents/CALL_CHAINS.zh.md",
        "expected/agents/DEPENDENCIES.md",
        "expected/agents/DEPENDENCIES.zh.md",
    ]
    for relative in expected_docs:
        assert (BUSINESS_FIXTURE / relative).exists(), f"missing expected doc: {relative}"

    detection = run_json([sys.executable, str(DETECTOR), str(BUSINESS_FIXTURE)])
    assert detection["matched_templates"] == ["baseline", "maven-java", "springboot3-webflux"]

    maven = run_json([sys.executable, str(MAVEN_INSPECTOR), str(BUSINESS_FIXTURE)])
    dependencies = {
        (dep["groupId"], dep["artifactId"])
        for dep in maven["pom_tree"]["dependencies"]
    }
    assert maven["pom_tree"]["properties"]["java.version"] == "17"
    assert maven["pom_tree"]["properties"]["maven.version"] == "3.4.0"
    assert ("org.springframework.boot", "spring-boot-starter-webflux") in dependencies
    assert ("org.springframework.boot", "spring-boot-starter-data-r2dbc") in dependencies
    assert ("org.springframework.boot", "spring-boot-starter-data-redis-reactive") in dependencies
    assert ("org.postgresql", "r2dbc-postgresql") in dependencies
    assert ("io.springfox", "springfox-boot-starter") in dependencies
    assert ("com.google.cloud", "spring-cloud-gcp-starter-pubsub") in dependencies


def main() -> int:
    run([sys.executable, "-m", "json.tool", str(ROOT / "evals" / "evals.json")])
    run(
        [
            sys.executable,
            "-m",
            "py_compile",
            str(DETECTOR),
            str(RENDERER),
            str(MAVEN_INSPECTOR),
            str(DEPS_TREE),
            str(SPRING_INSPECTOR),
            str(KARATE_INSPECTOR),
        ]
    )

    with tempfile.TemporaryDirectory(prefix="init-project-validate-") as temp_name:
        temp_root = Path(temp_name)
        validate_webflux(make_webflux(temp_root))
        validate_karate(make_karate(temp_root))
        maven_project, fake_mvn = make_multimodule(temp_root)
        validate_maven(maven_project, fake_mvn)
        validate_explicit_template(temp_root)

    validate_business_fixture()

    for cache in SCRIPT_DIR.rglob("__pycache__"):
        shutil.rmtree(cache)

    print("init-project validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
