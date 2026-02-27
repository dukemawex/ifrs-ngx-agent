const TINYFISH_SSE_URL = "https://agent.tinyfish.ai/v1/automation/run-sse";

export type TinyFishRunInput = {
  goal: string;
  browser_profile?: "stealth" | string;
  metadata?: Record<string, unknown>;
};

export type TinyFishRunResult = {
  rawEvents: unknown[];
  resultJson: unknown;
};

const decoder = new TextDecoder();

function extractJsonPayload(dataLine: string): unknown {
  try {
    return JSON.parse(dataLine);
  } catch {
    return dataLine;
  }
}

export async function runTinyFishAutomation(
  input: TinyFishRunInput,
  apiKey: string,
): Promise<TinyFishRunResult> {
  const response = await fetch(TINYFISH_SSE_URL, {
    method: "POST",
    headers: {
      "X-API-Key": apiKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ...input,
      browser_profile: input.browser_profile ?? "stealth",
    }),
  });

  if (!response.ok || !response.body) {
    throw new Error(`TinyFish SSE request failed: ${response.status} ${response.statusText}`);
  }

  const reader = response.body.getReader();
  let buffer = "";
  const rawEvents: unknown[] = [];
  let finalResult: unknown = null;

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split("\n\n");
    buffer = chunks.pop() ?? "";

    for (const chunk of chunks) {
      const lines = chunk.split("\n").map((l) => l.trim());
      for (const line of lines) {
        if (!line.startsWith("data:")) continue;
        const payloadStr = line.slice(5).trim();
        if (!payloadStr) continue;
        const payload = extractJsonPayload(payloadStr);
        rawEvents.push(payload);

        if (typeof payload === "object" && payload !== null) {
          const typed = payload as Record<string, unknown>;
          const status = String(typed.status ?? typed.event ?? "").toUpperCase();
          if (status.includes("COMPLETE")) {
            finalResult = typed.resultJson ?? typed.result ?? typed.data ?? finalResult;
          }
        }
      }
    }
  }

  if (finalResult === null && rawEvents.length > 0) {
    finalResult = rawEvents[rawEvents.length - 1];
  }

  return { rawEvents, resultJson: finalResult };
}
