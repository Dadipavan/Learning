
<h2 id="s21-9">21.9 LLM SDK Calls: Clients, Retries, Streaming and Structured Output</h2>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">Calling a hosted LLM is an HTTP request to a very busy shop. Sometimes the shop says "come back in two seconds" (429, rate limit), sometimes it is briefly broken (500, 503), sometimes it is slow (timeout). The answer arrives as text, not as a guaranteed data structure, so you must <em>check</em> it before trusting it. Good SDK code is therefore three layers: a request, a safety net around failures, and a validator around the reply.</div></div>
<h3>Reference: what you use from the OpenAI and Anthropic style SDKs</h3>
<div class="tablewrap"><table class="data"><thead><tr><th>Name</th><th>What it does in plain English</th><th>Minimal example (not run here)</th></tr></thead><tbody>
<tr><td><code>OpenAI(...)</code> / <code>anthropic.Anthropic(...)</code></td><td>Create a client; reads the API key from an environment variable</td><td><code>client = anthropic.Anthropic()</code></td></tr>
<tr><td><code>max_retries</code>, <code>timeout</code></td><td>Built-in retry count and request time limit</td><td><code>Anthropic(max_retries=3, timeout=30.0)</code></td></tr>
<tr><td><code>client.with_options(...)</code></td><td>Override settings for one call</td><td><code>client.with_options(timeout=5).messages.create(...)</code></td></tr>
<tr><td><code>client.messages.create</code> (Anthropic)</td><td>One chat turn: model, max_tokens, messages</td><td><code>create(model=M, max_tokens=500, messages=[...])</code></td></tr>
<tr><td><code>client.chat.completions.create</code> (OpenAI)</td><td>One chat turn in the OpenAI shape</td><td><code>create(model=M, messages=[...])</code></td></tr>
<tr><td><code>client.responses.create</code> (OpenAI)</td><td>OpenAI's newer unified endpoint</td><td><code>create(model=M, input="...")</code></td></tr>
<tr><td><code>system</code> / role <code>system</code></td><td>Standing instructions for the model</td><td><code>system="You label tickets."</code> (Anthropic), a system message (OpenAI)</td></tr>
<tr><td><code>response.content[0].text</code></td><td>Read the text of an Anthropic reply</td><td>check <code>stop_reason</code> first</td></tr>
<tr><td><code>response.choices[0].message.content</code></td><td>Read the text of an OpenAI reply</td><td>check <code>finish_reason</code> first</td></tr>
<tr><td><code>response.usage</code></td><td>Input and output token counts (cost)</td><td><code>usage.input_tokens</code>, <code>usage.output_tokens</code></td></tr>
<tr><td><code>stop_reason</code> / <code>finish_reason</code></td><td>Why generation ended: finished, hit the length limit, tool call, refusal</td><td><code>if r.stop_reason == "max_tokens": ...</code></td></tr>
<tr><td><code>client.messages.stream(...)</code></td><td>Stream text pieces as they arrive</td><td><code>for t in stream.text_stream: ...</code></td></tr>
<tr><td><code>stream=True</code> (OpenAI)</td><td>Iterate over chunks with <code>delta.content</code></td><td><code>for chunk in client.chat.completions.create(..., stream=True)</code></td></tr>
<tr><td><code>stream.get_final_message()</code></td><td>The full message after streaming (Anthropic)</td><td>use it to read usage and stop reason</td></tr>
<tr><td><code>messages.parse(..., output_format=Model)</code></td><td>Reply validated against a Pydantic model (Anthropic)</td><td><code>r.parsed_output</code></td></tr>
<tr><td><code>chat.completions.parse(response_format=Model)</code></td><td>Same idea for OpenAI</td><td><code>r.choices[0].message.parsed</code></td></tr>
<tr><td><code>tools=[...]</code></td><td>Describe functions the model may ask you to call</td><td>name, description, JSON schema</td></tr>
<tr><td><code>client.embeddings.create</code></td><td>Embedding vectors from a hosted model</td><td><code>create(model=E, input=[...])</code></td></tr>
<tr><td><code>RateLimitError</code></td><td>429: slow down; retry later</td><td><code>except anthropic.RateLimitError</code></td></tr>
<tr><td><code>APIStatusError</code></td><td>Any non-success HTTP status (has <code>status_code</code>)</td><td><code>e.status_code &gt;= 500</code></td></tr>
<tr><td><code>APIConnectionError / APITimeoutError</code></td><td>Network failure / no reply in time</td><td>retry</td></tr>
<tr><td><code>BadRequestError / AuthenticationError</code></td><td>Your bug or a bad key: do NOT retry</td><td>fix the request</td></tr>
<tr><td><code>AsyncOpenAI / AsyncAnthropic</code></td><td>Async clients for concurrency</td><td><code>await client.messages.create(...)</code></td></tr>
<tr><td><code>client.messages.count_tokens</code> (Anthropic)</td><td>Count tokens before sending</td><td>budget your prompt</td></tr>
</tbody></table></div>
<p>The following is the idiomatic, minimal shape of each call (not run here; no API key or network in this book). The model name is a placeholder: always read the provider's current model list rather than copying an id from a book.</p>
%%NORUN
import json
import anthropic
from pydantic import BaseModel

MODEL = "your-model-id"                      # choose from the provider's current model list
client = anthropic.Anthropic(max_retries=3, timeout=30.0)   # key read from ANTHROPIC_API_KEY

# 1) a plain call
resp = client.messages.create(
    model=MODEL, max_tokens=500,
    system="You are a support assistant. Answer in two sentences.",
    messages=[{"role": "user", "content": "How do I reset my password?"}],
)
if resp.stop_reason == "max_tokens":
    print("answer was cut off; raise max_tokens")
print(resp.content[0].text)
print(resp.usage.input_tokens, resp.usage.output_tokens)

# 2) streaming: print text as it arrives, then read the final message
with client.messages.stream(model=MODEL, max_tokens=500,
                            messages=[{"role": "user", "content": "Draft a reply to a billing complaint."}]) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()
print("\ntokens out:", final.usage.output_tokens)

# 3) structured output: the SDK validates the reply against a Pydantic model
class TicketLabel(BaseModel):
    label: str            # billing | bug | how-to
    urgency: int          # 1 to 5
    summary: str

parsed = client.messages.parse(
    model=MODEL, max_tokens=500,
    messages=[{"role": "user", "content": "Classify: 'I was charged twice and need money back today.'"}],
    output_format=TicketLabel,
)
print(parsed.parsed_output)       # a TicketLabel instance, not a string

# 4) errors: most specific first
try:
    client.messages.create(model=MODEL, max_tokens=50, messages=[{"role": "user", "content": "hi"}])
except anthropic.RateLimitError as e:
    print("rate limited, retry after", e.response.headers.get("retry-after"))
except anthropic.APIConnectionError:
    print("network problem")
except anthropic.APIStatusError as e:
    print("server said", e.status_code)
%%END
<p>The OpenAI client has the same bones with different names (not run here):</p>
%%NORUN
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(max_retries=3, timeout=30.0)            # key from OPENAI_API_KEY
MODEL = "your-model-id"

resp = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "system", "content": "You label support tickets."},
              {"role": "user", "content": "I was charged twice."}],
)
print(resp.choices[0].message.content, resp.choices[0].finish_reason, resp.usage.total_tokens)

stream = client.chat.completions.create(model=MODEL, stream=True,
                                         messages=[{"role": "user", "content": "Write a short apology."}])
for chunk in stream:
    delta = chunk.choices[0].delta.content          # may be None on the first and last chunk
    if delta:
        print(delta, end="", flush=True)

class TicketLabel(BaseModel):
    label: str
    urgency: int

r = client.chat.completions.parse(model=MODEL, response_format=TicketLabel,
                                  messages=[{"role": "user", "content": "Classify: app crashes on login"}])
print(r.choices[0].message.parsed)
%%END
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Both SDKs already retry connection errors, 429 and 5xx responses with exponential backoff (a small default number of times; check the current default in the docs). Set <code>max_retries</code> and <code>timeout</code> on the client first. Write your own retry loop only for behaviour the SDK does not offer, and never stack a retry loop of five on top of an SDK retry of three without realising that you now make up to twenty attempts.</div></div>
<h3>Worked example: retries with exponential backoff and jitter</h3>
<p>The logic behind SDK retries is simple and worth knowing. After a failure wait <code>base x 2<sup>attempt</sup></code> seconds (capped), but choose a <em>random</em> number between 0 and that value (<strong>full jitter</strong>). Without randomness, a hundred clients that failed together all retry together and fail again. If the server sends a <code>retry-after</code> header, obey it. Errors caused by your own request (400, 401, 403, 404) must never be retried because the answer will not change.</p>
<p>A fake client with scripted failures lets us test this exactly. Time is simulated by passing in a <code>sleep</code> function that records the wait instead of waiting.</p>
<p class="problem"><span class="pl">Problem 21.9.1</span> Script three situations: (A) a 429 with <code>retry-after</code> 2 seconds, then a 503, then success; (B) a 400 error; (C) six 503 errors in a row with a retry limit of 4. Show the waits and the outcome of each.</p>
%%PY
import random
from dataclasses import dataclass

class APIStatusError(Exception):
    def __init__(self, status_code, retry_after=None):
        super().__init__(f"HTTP {status_code}")
        self.status_code, self.retry_after = status_code, retry_after
class RateLimitError(APIStatusError): pass
class InternalServerError(APIStatusError): pass
class BadRequestError(APIStatusError): pass
class APITimeoutError(Exception): pass

@dataclass
class Response:
    text: str
    input_tokens: int
    output_tokens: int

class FakeLLM:
    """Plays back a script of outcomes: an exception instance to raise, or a string to return."""
    def __init__(self, script):
        self.script, self.calls = list(script), 0
    def complete(self, prompt):
        self.calls += 1
        outcome = self.script.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return Response(outcome, input_tokens=len(prompt.split()), output_tokens=len(outcome.split()))

RETRYABLE = (RateLimitError, InternalServerError, APITimeoutError)

def call_with_retries(fn, max_retries=4, base=0.5, cap=8.0, sleep=None, rng=None):
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except RETRYABLE as e:
            if attempt == max_retries:
                raise
            hinted = getattr(e, "retry_after", None)
            delay = hinted if hinted is not None else rng.uniform(0, min(cap, base * 2 ** attempt))
            sleep(delay)
        # BadRequestError is not in RETRYABLE, so it propagates immediately

def run(label, script):
    waits, llm = [], FakeLLM(script)
    try:
        r = call_with_retries(lambda: llm.complete("label this ticket please"),
                              sleep=waits.append, rng=random.Random(0))
        outcome = f"ok: {r.text!r}"
    except Exception as e:
        outcome = f"gave up: {type(e).__name__} ({e})"
    print(f"{label}: calls={llm.calls} waits={[round(w, 2) for w in waits]} -> {outcome}")

run("A", [RateLimitError(429, retry_after=2.0), InternalServerError(503), "billing"])
run("B", [BadRequestError(400), "never reached"])
run("C", [InternalServerError(503)] * 6)
%%END
<ol><li>The exception classes copy the names used by the real SDKs, so this code reads like the real thing. <code>RETRYABLE</code> is the allow-list of failures worth another try: 429, 5xx and timeouts.</li><li><code>FakeLLM</code> returns the next scripted outcome. This is the standard way to unit-test LLM code without a network: deterministic, free and instant.</li><li><code>call_with_retries</code> loops up to <code>max_retries + 1</code> times. On a retryable failure it uses the server's <code>retry-after</code> hint when present, otherwise a random wait between 0 and <code>min(cap, base x 2<sup>attempt</sup>)</code>. The last attempt re-raises instead of waiting.</li><li>Scenario A makes three calls. The first wait is exactly 2.0 (the hint); the second is a random value below 1.0 (attempt 1 allows up to 0.5 x 2 = 1.0). Then the success text comes back.</li><li>Scenario B stops after one call and no wait: a 400 is your bug, and retrying cannot fix it.</li><li>Scenario C makes five calls (the first plus four retries), waits four times, each a random value below a doubling ceiling (0.5, 1.0, 2.0, 4.0), and finally raises. Callers must handle that final failure: a fallback model, a cached answer, or a clear error for the user.</li><li>Injecting <code>sleep</code> and <code>rng</code> is what made the test possible. In production pass <code>time.sleep</code> and a <code>random.Random()</code>.</li></ol>
<figure><img src="images/lib21_retry_backoff.png" alt="Bar chart of the maximum wait allowed for each retry attempt with exponential growth capped at 8 seconds, plus dots for sampled jittered waits" loading="lazy"/><figcaption>Figure 21.8. Exponential backoff ceilings (bars) and sampled full-jitter waits (dots) for attempts 0 to 6, with base 0.5 s and cap 8 s.</figcaption></figure>
<p><strong>How to read it:</strong> each bar is the longest wait allowed before the next attempt, doubling until it hits the cap. Each dot is one random wait actually drawn. The scatter of the dots is the point: different clients wake up at different moments, so they do not hit the server in one wave.</p>
<h3>Streaming</h3>
<p>A long answer takes many seconds. Streaming returns it in small pieces so a user sees the first words almost at once, and it avoids request timeouts on long outputs. A stream is just a Python generator that yields text pieces. Three things matter: accumulate the pieces into the full text, handle a failure in the middle (the partial text is usually unusable; restart or fall back), and read the usage numbers at the end.</p>
%%PY
import time

class FakeStreamingLLM:
    def __init__(self, text, fail_after=None):
        self.text, self.fail_after = text, fail_after
    def stream(self, prompt):
        words = self.text.split()
        for i, w in enumerate(words):
            if self.fail_after is not None and i == self.fail_after:
                raise ConnectionError("connection dropped mid-stream")
            yield w + (" " if i < len(words) - 1 else "")

def consume(stream_fn, on_piece=None):
    parts = []
    try:
        for piece in stream_fn():
            parts.append(piece)
            if on_piece:
                on_piece(piece)
        return "".join(parts), True
    except ConnectionError:
        return "".join(parts), False          # partial text plus a flag

reply = "Please reset your password using the link on the sign in page"
shown = []
text, ok = consume(lambda: FakeStreamingLLM(reply).stream("q"), on_piece=shown.append)
print("pieces:", len(shown), "| first piece:", repr(shown[0]), "| complete:", ok)
print("joined equals original:", text == reply)

text, ok = consume(lambda: FakeStreamingLLM(reply, fail_after=4).stream("q"))
print("failed stream ->", repr(text), "| complete:", ok)

def stream_with_fallback(prompt, attempts):
    for llm in attempts:                       # restart from scratch on a new attempt
        text, ok = consume(lambda: llm.stream(prompt))
        if ok:
            return text
    return None
print("recovered:", stream_with_fallback("q", [FakeStreamingLLM(reply, fail_after=2), FakeStreamingLLM(reply)]) == reply)
%%END
<ol><li>The fake <code>stream</code> method is a generator: each <code>yield</code> hands one piece to the caller and pauses. Real SDK streams (<code>stream.text_stream</code>, or iterating OpenAI chunks) behave the same way.</li><li><code>consume</code> collects pieces in a list and joins once at the end. Joining a list is faster than repeatedly appending to a string; <code>on_piece</code> is where a web server would forward each piece to the browser.</li><li>The first run shows 12 pieces (one per word) and proves that joining them reproduces the exact reply.</li><li>The second run simulates a dropped connection after four words. The function returns the partial text and <code>False</code>. A partial JSON document or half a sentence must not be treated as a result.</li><li>The third part retries from scratch with a fresh stream, because a stream cannot be resumed from the middle in general. It recovers on the second attempt.</li><li>In real SDK code you do the same inside a <code>with client.messages.stream(...)</code> block, catch the connection exception, and read token usage from the final message once the stream completes.</li></ol>
<h3>Structured output: never trust the shape of a reply</h3>
<p>You want <code>{"label": "billing", "urgency": 4}</code> and sometimes get a fenced code block, a trailing comma, a missing key or a number as a string. There are three defences, strongest first: (1) use the provider's structured output feature (schema-constrained decoding, or <code>parse()</code> with a Pydantic model) so the reply is valid by construction; (2) validate every reply yourself against the schema; (3) on failure, retry once or twice with the validation error in the prompt (a <em>repair loop</em>). Even with (1), still check <code>stop_reason</code>: a reply cut off by <code>max_tokens</code> is incomplete and refusals are not data.</p>
%%PY
import json, re
from dataclasses import dataclass

LABELS = {"billing", "bug", "how-to"}

class ValidationFailure(Exception):
    pass

@dataclass
class TicketLabel:
    label: str
    urgency: int

def parse_label(raw):
    text = raw.strip()
    fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)       # models like to add code fences
    if fenced:
        text = fenced.group(1)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValidationFailure(f"not valid JSON: {e.msg}")
    if not isinstance(data, dict):
        raise ValidationFailure("expected a JSON object")
    missing = {"label", "urgency"} - data.keys()
    if missing:
        raise ValidationFailure(f"missing keys: {sorted(missing)}")
    if data["label"] not in LABELS:
        raise ValidationFailure(f"label must be one of {sorted(LABELS)}, got {data['label']!r}")
    if not isinstance(data["urgency"], int) or isinstance(data["urgency"], bool) or not 1 <= data["urgency"] <= 5:
        raise ValidationFailure("urgency must be an integer from 1 to 5")
    return TicketLabel(data["label"], data["urgency"])

class ScriptedModel:
    def __init__(self, replies):
        self.replies, self.prompts = list(replies), []
    def complete(self, prompt):
        self.prompts.append(prompt)
        return self.replies.pop(0)

def classify(model, ticket, max_attempts=3):
    prompt = f"Return JSON with label and urgency for: {ticket}"
    for attempt in range(1, max_attempts + 1):
        raw = model.complete(prompt)
        try:
            return parse_label(raw), attempt
        except ValidationFailure as e:
            prompt = f"{prompt}\nYour last reply was rejected: {e}. Return only valid JSON."
    raise ValidationFailure("gave up after repairs")

replies = [
    '{"label": "billing", "urgency": 4,}',                     # trailing comma
    '```json\n{"label": "refund", "urgency": 4}\n```',          # fenced, bad label
    '{"label": "billing", "urgency": "high"}',                  # wrong type
    '{"label": "billing", "urgency": 4}',
]
m = ScriptedModel(replies)
try:
    result, attempts = classify(m, "charged twice", max_attempts=3)
except ValidationFailure as e:
    print("3 attempts failed:", e)
m = ScriptedModel(replies[1:])
result, attempts = classify(m, "charged twice", max_attempts=3)
print("result:", result, "after", attempts, "attempts")
print("last prompt tail:", m.prompts[-1].splitlines()[-1])
print("fenced valid reply parses:", parse_label('```json\n{"label": "bug", "urgency": 2}\n```'))
%%END
<ol><li><code>parse_label</code> is a defensive parser: strip whitespace, remove a code fence if present, <code>json.loads</code>, then check type, required keys, allowed values and ranges. Each failure raises one exception with a human-readable reason.</li><li><code>isinstance(True, int)</code> is true in Python, so the explicit <code>bool</code> check stops <code>true</code> from passing as urgency 1.</li><li><code>classify</code> is the repair loop. After a rejection it appends the reason to the prompt, which gives the model the information it needs to fix the reply.</li><li>First we feed the script of four replies with only three attempts allowed: the first three are all invalid (trailing comma, unknown label, wrong type) so it fails and prints the message "3 attempts failed".</li><li>Then we start from the second reply, giving a bad label, a bad type, then a good reply: success on attempt 3. The last prompt shows the accumulated rejection notes.</li><li>The final line shows the fence-stripping path working. With provider-side structured outputs most of these failures disappear, but the validator stays as the last line of defence, because it is cheap and the cost of trusting a malformed reply is high.</li></ol>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Wrong:</strong> <code>data = json.loads(resp.content[0].text)</code> with no checks. <strong>Symptom:</strong> works in the demo, then a production request returns a refusal, a truncated answer or a code fence and the job crashes with <code>JSONDecodeError</code>, or worse, a wrong-typed value silently flows into your database. <strong>Fix:</strong> check the stop reason, use the provider's structured output feature or <code>parse()</code>, validate against a schema, and bound the number of repairs.</div></div>
<h3>Tool calls, rate limits and cost</h3>
<p>When you give a model <strong>tools</strong>, it can reply "please call <code>lookup_ticket</code> with id 7" instead of text. You run the function and send the result back; the loop ends when the model answers in text. Keep a hard cap on loop turns. Two more production basics: a <strong>token bucket</strong> to stay under rate limits, and a <strong>cost estimate</strong> from the usage numbers. Prices below are invented for illustration; read your provider's price page.</p>
%%PY
import json

TICKETS = {7: {"status": "open", "plan": "pro"}, 9: {"status": "closed", "plan": "free"}}
def lookup_ticket(ticket_id):
    return TICKETS.get(ticket_id, {"error": "not found"})
TOOLS = {"lookup_ticket": lookup_ticket}

class ScriptedToolModel:
    """Turn 1 asks for a tool; turn 2 answers using the tool result."""
    def __init__(self):
        self.turn = 0
    def respond(self, messages):
        self.turn += 1
        if self.turn == 1:
            return {"type": "tool_call", "name": "lookup_ticket", "arguments": {"ticket_id": 7}}
        last = json.loads(messages[-1]["content"])
        return {"type": "text", "text": f"Ticket 7 is {last['status']} on the {last['plan']} plan."}

def agent_loop(model, question, max_turns=5):
    messages = [{"role": "user", "content": question}]
    for _ in range(max_turns):                                  # hard cap against endless loops
        out = model.respond(messages)
        if out["type"] == "text":
            return out["text"], messages
        fn = TOOLS.get(out["name"])
        result = fn(**out["arguments"]) if fn else {"error": "unknown tool"}
        messages.append({"role": "assistant", "content": f"call {out['name']}"})
        messages.append({"role": "tool", "content": json.dumps(result)})
    return "stopped: too many tool turns", messages

answer, msgs = agent_loop(ScriptedToolModel(), "What is the state of ticket 7?")
print(answer)
print("roles:", [m["role"] for m in msgs])

class TokenBucket:
    def __init__(self, rate_per_s, capacity):
        self.rate, self.capacity, self.tokens, self.t = rate_per_s, capacity, capacity, 0.0
    def allow(self, now, cost=1):
        self.tokens = min(self.capacity, self.tokens + (now - self.t) * self.rate)
        self.t = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

bucket = TokenBucket(rate_per_s=2, capacity=3)
times = [0.0, 0.1, 0.2, 0.3, 0.4, 1.0, 1.1]
print("allowed:", [bucket.allow(t) for t in times])

def cost_usd(inp, out, price_in_per_m=3.0, price_out_per_m=15.0):      # illustrative prices only
    return inp / 1e6 * price_in_per_m + out / 1e6 * price_out_per_m
print("10000 calls x (800 in, 150 out):", round(10000 * cost_usd(800, 150), 2), "dollars at the invented prices")
%%END
<ol><li>The agent loop is the whole idea of tool use: ask the model, if it requests a tool then run it and append the result, ask again. The <code>max_turns</code> cap protects against a model that keeps calling tools forever.</li><li>Unknown tool names return an error result instead of crashing; the model can read the error and try something else.</li><li>The printed roles show the conversation order: user, then the assistant's tool request, then the tool result.</li><li>The token bucket holds up to 3 tokens and refills at 2 per second. The five calls at 0.0 to 0.4 seconds use the bucket up: the first three pass and the next two are refused (the refill of 0.2 and 0.4 tokens is not enough). By 1.0 s enough has refilled that the next call passes. Refused calls should wait, not be dropped silently.</li><li>Cost is linear in tokens: 800 x 3.0 / 1e6 + 150 x 15.0 / 1e6 = 0.00465 per call, so 10,000 calls cost 46.5 dollars at these invented prices. Always multiply per-call cost by your real daily volume before building.</li></ol>
