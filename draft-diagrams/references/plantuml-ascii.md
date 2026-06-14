# PlantUML ASCII Diagrams

Use PlantUML text mode when the user needs a diagram that works in terminals, plain-text emails, code comments, changelogs, or other contexts where graphical rendering is not available.

PlantUML ASCII is best for compact sequence, class, activity, state, component, use case, and deployment diagrams. Complex diagrams can become hard to read in fixed-width text; suggest Mermaid or image export when the diagram grows.

## File Shape

```plantuml
@startuml
actor User
participant "API Service" as API
database "Database" as DB

User -> API : Request
API -> DB : Query
DB --> API : Result
API --> User : Response
@enduml
```

## Generate Text Output

```bash
plantuml -txt diagram.puml
plantuml -utxt diagram.puml
```

Output files:

- `diagram.atxt` for pure ASCII.
- `diagram.utxt` for Unicode box-drawing output.

Prefer `-utxt` when the destination supports UTF-8 and fixed-width fonts. Prefer `-txt` for maximum portability.

## Useful Templates

Sequence:

```plantuml
@startuml
actor User
participant "Web App" as Web
participant "API Service" as API
database "Orders DB" as DB

User -> Web : Submit order
Web -> API : POST /orders
API -> DB : Insert order
DB --> API : order_id
API --> Web : 201 Created
Web --> User : Show confirmation
@enduml
```

Class:

```plantuml
@startuml
class User {
  +id: string
  +email: string
  +login(): Session
}

class Order {
  +id: string
  +total: Money
  +submit()
}

User "1" -- "*" Order : places
@enduml
```

Activity:

```plantuml
@startuml
start
:Receive request;
if (Valid?) then (yes)
  :Process command;
  :Persist result;
else (no)
  :Return validation error;
  stop
endif
:Return success;
stop
@enduml
```

Component:

```plantuml
@startuml
[Web App] as web
[API Service] as api
[Worker] as worker
database "Orders DB" as db
queue "Order Events" as events

web --> api
api --> db
api --> events
events --> worker
worker --> db
@enduml
```

## Practical Guidance

- Keep labels short. Long labels break alignment and readability.
- Use aliases for names with spaces: `"API Service" as API`.
- Verify output in a fixed-width font before sharing.
- Use Mermaid when the diagram must render directly in Markdown.
- Use PlantUML source plus generated text output when the user wants both maintainability and copy-pasteable ASCII.

