# Final Architecture Diagrams

These diagrams describe the connected request path. PostgreSQL, Redis, Chroma, RAG, booking, and live travel providers are not part of that path.

## System view

```mermaid
flowchart LR
    UI[Vue recruiter demo] --> API[FastAPI plan endpoint]
    API --> S[TravelService]
    S --> P[Deterministic parser]
    P --> G[Coverage gate]
    G -->|covered| R[Canonical requirements]
    G -->|gap + hybrid| X[Structured semantic extractor]
    X --> M[Conservative merge]
    M --> R
    R --> L[Single LangGraph agent]
    L --> T[Typed search tools]
    T --> D[Controlled 12-city data]
    L --> B[Deterministic budget tool]
    B --> V[Typed validator]
    V --> O[Allowlisted public response]
    O --> UI
```

## Runtime state machine

```mermaid
flowchart TD
    START --> Preflight
    Preflight -->|missing destination/duration| Clarification --> END
    Preflight -->|sufficient| Planner
    Planner --> Tools
    Tools --> Validate
    Validate -->|pass| Finalize
    Validate -->|eligible hard-budget violation and no prior repair| Replan
    Replan --> Planner
    Validate -->|not repairable or second failure| Finalize
    Finalize --> END
```

`Replan` carries typed violations and the prior itinerary. The routing condition caps it at one attempt.

## Semantic safety boundary

```mermaid
flowchart TD
    Q[Request] --> DP[Deterministic parse]
    DP --> CG{Coverage gap?}
    CG -->|No| CR[Canonical requirements]
    CG -->|Yes, deterministic mode| EX[Expose reason; no model call]
    CG -->|Yes, hybrid mode| SP[Untrusted structured proposal]
    SP --> GR{Grounded in source?}
    GR -->|No| RJ[Reject]
    GR -->|Yes| CP{Compatible scope, strength, polarity, correction target?}
    CP -->|Yes| AC[Accept bounded addition/replacement]
    CP -->|No| CQ[Conflict or clarification quarantine]
    EX --> CR
    RJ --> CR
    AC --> CR
    CQ --> CR
```

The model has no authority to calculate costs, select candidates, validate constraints, or decide repair eligibility.

## Public observability boundary

```mermaid
flowchart LR
    Internal[Internal state and trace] --> Allowlist[Explicit Pydantic projection]
    Allowlist --> Public[Stages, mode, tools, candidates, validation, repair facts]
    Internal -. excluded .-> Private[Prompts, raw provider response, hidden metadata, exceptions]
```

The UI receives completed facts, not hidden reasoning or fabricated live progress.

## Deployment status

```mermaid
flowchart LR
    Browser --> Vite[Vite dev server :5173]
    Vite -->|/api proxy| FastAPI[Uvicorn/FastAPI :8000]
    FastAPI --> Files[Checked-in JSON candidates]
    FastAPI -. optional hybrid/planner .-> OpenAI[OpenAI Responses API]
    FastAPI -. not used by planning path .-> Infra[PostgreSQL / Redis / Chroma]
```

The primary demo uses only Browser → Vite → FastAPI → checked-in data. It does not require Docker or an API key.
