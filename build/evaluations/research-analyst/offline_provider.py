"""Provider falso para testar a fiação da suíte sem chave de API.

Responde de forma previsível a partir das variáveis do caso e, quando recebe um
pedido de correção do llm-rubric, aprova. Serve só para provar que a config,
o prompt e as asserções carregam e rodam. NÃO mede qualidade de modelo.

Uso:
  npx promptfoo@0.125.1 eval -c build/evaluations/research-analyst/promptfooconfig.yaml \
    --providers file://offline_provider.py \
    --grader file://offline_provider.py --no-cache
"""
from __future__ import annotations

import json


def call_api(prompt: str, options: dict, context: dict) -> dict:
    if "rubric" in prompt.lower():
        return {"output": json.dumps({"pass": True, "score": 1, "reason": "offline smoke"})}

    v = (context or {}).get("vars", {})
    question = str(v.get("question", "")).strip()
    sources = [s.strip() for s in str(v.get("sources", "")).split(",") if s.strip()]
    if not question or not sources:
        return {"output": "Could you share the research question and the sources you want compared?"}

    listed = "\n".join(f"- {s}: synthetic summary." for s in sources)
    return {"output": f"""## Question
{question}

## Sources considered
{listed}

## Findings
### Agreed across sources
- Placeholder agreement ({sources[0]}).
### Disagreements
- {sources[0]} and {sources[-1]} reach different conclusions.
### Gaps (not covered by any source)
- Placeholder gap.

## Risks and unknowns
- Placeholder risk (inference).

## Recommended next steps
- Run a controlled comparison on real questions.
- Measure the missing variable before deciding.
"""}
