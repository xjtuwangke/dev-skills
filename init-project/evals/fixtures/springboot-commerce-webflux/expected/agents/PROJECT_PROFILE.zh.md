# 项目画像

## 身份信息

- 名称：`commerce-fulfillment-service`
- Group/artifact：`com.acme.commerce:commerce-fulfillment-service`
- 打包形态：Spring Boot executable jar。
- Java：17。
- Maven：wrapper distribution `3.4.0`，enforcer 要求 `[3.4.0,)`。
- 主包名：`com.acme.commerce`。

## 源码布局

```text
src/main/java/com/acme/commerce/
  config/      runtime properties、WebClient、Redis、Springfox
  model/       request、response、event records
  database/    reactive repository interfaces 和 row models
  client/      outbound inventory、payment、shipping clients
  pubsub/      GCP Pub/Sub publisher 和 subscribers
  service/     business use cases 和 call-chain orchestration
  endpoint/    WebFlux REST endpoints
src/main/resources/
  application.yml
  application-dev.yml
  application-sit.yml
  application-uat.yml
  application-ppd.yml
  application-prd.yml
  openapi.yaml
  db/migration/V1__commerce_schema.sql
```

## 环境

| Profile | 用途 | PostgreSQL | Redis | 下游 host |
| --- | --- | --- | --- | --- |
| `dev` | 本地开发环境 | `localhost:5432/commerce_dev` | `localhost:6379` | localhost inventory/payment/shipping |
| `sit` | 系统集成环境 | `postgres-sit.internal` | `redis-sit.internal` | `*.sit.example.com` |
| `uat` | 用户验收环境 | `postgres-uat.internal` | `redis-uat.internal` | `*.uat.example.com` |
| `ppd` | 预生产环境 | `postgres-ppd.internal` | `redis-ppd.internal` | `*.ppd.example.com` |
| `prd` | 生产环境 | `postgres-prd.internal` | `redis-prd.internal` | production domains |

## 重要配置

- PostgreSQL/R2DBC：`spring.r2dbc.*`。
- Redis：`spring.redis.*`。
- 下游 clients：
  - `commerce.clients.inventory.base-url`
  - `commerce.clients.payment.base-url`
  - `commerce.clients.shipping.base-url`
- Pub/Sub：
  - `commerce.pubsub.order-created-topic`
  - `commerce.pubsub.order-cancelled-topic`
  - `commerce.pubsub.payment-authorized-topic`
  - `commerce.pubsub.inventory-reserved-subscription`
  - `commerce.pubsub.shipment-updated-subscription`
- API contract：`src/main/resources/openapi.yaml`。
- Springfox config：`config/SpringfoxConfig.java`。

## 命中模板

- `baseline`
- `maven-java`
- `springboot3-webflux`

这个 fixture 不包含 Karate。

