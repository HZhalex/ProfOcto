import { useState, useRef, useEffect } from "react";
import { TOPIC_LIBRARY } from "./topics.js";

const PROF_COLORS = ["#4fc3f7", "#81c784", "#ffb74d", "#f48fb1", "#ce93d8"];
const ROLE_ICONS = {
  Empiricist: "📊",
  Theorist: "📐",
  Skeptic: "🔍",
  Pragmatist: "🔧",
  Historian: "📚",
};
const STATUS_STYLE = {
  VERIFIED: { color: "#66bb6a", symbol: "✓" },
  UNVERIFIED: { color: "#ffa726", symbol: "?" },
  CONTESTED: { color: "#ef5350", symbol: "✗" },
  OPINION: { color: "#9e9e9e", symbol: "◈" },
};

// ── Topic Library Panel ───────────────────────────────────────────────────────
function TopicLibrary({ onSelect }) {
  const [open, setOpen] = useState(null);
  return (
    <div style={s.libWrap}>
      <div style={s.libTitle}>📚 Topic Library</div>
      {TOPIC_LIBRARY.map((cat, i) => (
        <div key={i}>
          <div style={s.libCat} onClick={() => setOpen(open === i ? null : i)}>
            <span>{cat.field}</span>
            <span style={s.libChevron}>{open === i ? "▾" : "▸"}</span>
          </div>
          {open === i &&
            cat.topics.map((t, j) => (
              <div
                key={j}
                style={s.libTopic}
                onClick={() => onSelect(t, cat.field)}
              >
                {t}
              </div>
            ))}
        </div>
      ))}
    </div>
  );
}

// ── History Panel ─────────────────────────────────────────────────────────────
function HistoryPanel({ onView }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/history")
      .then((r) => r.json())
      .then((d) => {
        setSessions(d.sessions || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div style={s.histEmpty}>Loading...</div>;
  if (!sessions.length)
    return <div style={s.histEmpty}>No debates yet.</div>;

  return (
    <div style={s.histWrap}>
      <div style={s.libTitle}>🕘 History</div>
      {sessions.map((sess, i) => (
        <div key={i} style={s.histCard} onClick={() => onView(sess)}>
          <div style={s.histTopic}>{sess.topic || "(no topic)"}</div>
          <div style={s.histMeta}>
            {sess.field} · {sess.date?.slice(0, 10)}
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Transcript Viewer ─────────────────────────────────────────────────────────
function TranscriptViewer({ session, onBack }) {
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/history/${session.filename}`)
      .then((r) => r.json())
      .then((d) => {
        setContent(d.content || "");
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [session.filename]);

  return (
    <div style={s.transcriptWrap}>
      <button style={s.backBtn} onClick={onBack}>
        ← Back
      </button>
      <h2 style={s.transcriptTitle}>{session.topic}</h2>
      <div style={s.transcriptMeta}>
        {session.field} · {session.date?.slice(0, 10)}
      </div>
      {loading ? (
        <div style={s.histEmpty}>Loading...</div>
      ) : (
        <pre style={s.transcriptContent}>{content}</pre>
      )}
    </div>
  );
}

// ── Setup Form ────────────────────────────────────────────────────────────────
function SetupForm({ onStart }) {
  const [field, setField] = useState("Distributed / Efficient LLM");
  const [topic, setTopic] = useState(
    "Tensor Parallelism vs Pipeline Parallelism vs MoE: what is the best strategy to scale LLMs to trillions of parameters?",
  );
  const [tab, setTab] = useState("new"); // new | library | history
  const [viewSession, setViewSession] = useState(null);

  const handleSelect = (t, f) => {
    setTopic(t);
    setField(f);
    setTab("new");
  };

  if (viewSession) {
    return (
      <TranscriptViewer
        session={viewSession}
        onBack={() => setViewSession(null)}
      />
    );
  }

  return (
    <div style={s.setupOuter}>
      <div style={s.setupLeft}>
        <h1 style={s.logo}>⚔ Academic Debate Arena</h1>
        <p style={s.subtitle}>
          Learn by debating with top AI professors
        </p>

        <div style={s.tabs}>
          {["new", "library", "history"].map((t) => (
            <button
              key={t}
              style={{ ...s.tab, ...(tab === t ? s.tabActive : {}) }}
              onClick={() => setTab(t)}
            >
              {t === "new"
                ? "✏ New"
                : t === "library"
                  ? "📚 Library"
                  : "🕘 History"}
            </button>
          ))}
        </div>

        {tab === "new" && (
          <div style={s.form}>
            <label style={s.label}>Research field</label>
            <input
              style={s.input}
              value={field}
              onChange={(e) => setField(e.target.value)}
            />
            <label style={s.label}>Debate question</label>
            <textarea
              style={{ ...s.input, height: 90, resize: "vertical" }}
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
            <button style={s.btn} onClick={() => onStart(topic, field)}>
              🚀 Start debate
            </button>
          </div>
        )}

        {tab === "library" && <TopicLibrary onSelect={handleSelect} />}

        {tab === "history" && <HistoryPanel onView={setViewSession} />}
      </div>
    </div>
  );
}

// ── Debate Components ─────────────────────────────────────────────────────────
function ProfessorCard({ prof, color }) {
  return (
    <div style={{ ...s.profCard, borderLeftColor: color }}>
      <div style={{ ...s.profAvatar, background: color + "22", color }}>
        {ROLE_ICONS[prof.role] || "👤"}
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ ...s.profName, color }}>{prof.name}</div>
        <div style={s.profUni}>{prof.university}</div>
        <div style={s.profRole}>{prof.role}</div>
        <div style={s.profStance}>{prof.stance}</div>
      </div>
    </div>
  );
}

function FactTag({ tag }) {
  const st = STATUS_STYLE[tag.status] || STATUS_STYLE.OPINION;
  return (
    <div style={s.factRow}>
      <span
        style={{
          ...s.factBadge,
          color: st.color,
          borderColor: st.color + "44",
        }}
      >
        {st.symbol} {tag.status}
      </span>
      <span style={s.factClaim}>{tag.claim}</span>
      {tag.reason && <span style={s.factReason}> — {tag.reason}</span>}
      {tag.sources?.map((src, i) => (
        <div key={i} style={s.factSource}>
          ↳ {src}
        </div>
      ))}
    </div>
  );
}

function TurnBubble({ turn, professors }) {
  const profIdx = professors.findIndex((p) => p.key === turn.key);
  const color = PROF_COLORS[profIdx] || "#aaa";

  if (turn.type === "round")
    return <div style={s.roundDivider}>── Round {turn.round} ──</div>;

  if (turn.type === "moderator")
    return (
      <div style={s.modBubble}>
        <div style={s.modLabel}>🎯 {turn.label}</div>
        <div style={s.modContent}>{turn.content}</div>
      </div>
    );

  if (turn.type === "final")
    return (
      <div style={s.finalWrap}>
        <div style={s.finalTitle}>🏁 Key Insights</div>
        {turn.content.split("\n").map((line, i) => (
          <div
            key={i}
            style={
              line.startsWith("**")
                ? s.finalSection
                : line.startsWith("-")
                  ? s.finalBullet
                  : s.finalLine
            }
          >
            {line.replace(/\*\*/g, "")}
          </div>
        ))}
      </div>
    );

  if (turn.type === "research_kit")
    return (
      <div style={s.researchWrap}>
        <div style={s.researchTitle}>📚 Research Kit for Paper</div>

        <div style={s.researchSection}>
          <div style={s.researchHeading}>📄 Paper Outline</div>
          <pre style={s.researchContent}>{turn.outline}</pre>
        </div>

        {turn.key_findings?.length > 0 && (
          <div style={s.researchSection}>
            <div style={s.researchHeading}>🔍 Key Findings</div>
            {turn.key_findings.map((f, i) => (
              <div key={i} style={s.findingItem}>
                <div style={s.findingText}>
                  <strong>{f.finding}</strong>
                </div>
                <div style={s.findingEvidence}>Evidence: {f.evidence}</div>
                <div style={s.findingImpact}>Impact: {f.impact}</div>
              </div>
            ))}
          </div>
        )}

        {turn.open_questions?.length > 0 && (
          <div style={s.researchSection}>
            <div style={s.researchHeading}>❓ Open Research Questions</div>
            <ol style={{ marginLeft: 20, color: "#bbb" }}>
              {turn.open_questions.map((q, i) => (
                <li key={i} style={{ marginBottom: 6 }}>
                  {q}
                </li>
              ))}
            </ol>
          </div>
        )}

        {turn.recommendations?.length > 0 && (
          <div style={s.researchSection}>
            <div style={s.researchHeading}>
              💡 Recommendations for Next Steps
            </div>
            <ul style={{ marginLeft: 20, color: "#bbb" }}>
              {turn.recommendations.map((r, i) => (
                <li key={i} style={{ marginBottom: 6 }}>
                  {r}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );

  return (
    <div style={{ ...s.turnWrap, borderLeftColor: color }}>
      <div style={s.turnHeader}>
        <span style={{ ...s.turnName, color }}>{turn.name}</span>
        <span style={s.turnRole}>{turn.role}</span>
        <span style={s.turnNum}>Turn {turn.turn}</span>
      </div>
      <div style={s.turnContent}>
        {turn.content}
        {turn.streaming && <span style={s.cursor}>▍</span>}
      </div>
      {turn.fact_tags?.length > 0 && (
        <div style={s.factWrap}>
          {turn.fact_tags.map((t, i) => (
            <FactTag key={i} tag={t} />
          ))}
        </div>
      )}
    </div>
  );
}

// ── Main App ──────────────────────────────────────────────────────────────────
export default function App() {
  const [phase, setPhase] = useState("setup");
  const [status, setStatus] = useState("");
  const [professors, setProfessors] = useState([]);
  const [turns, setTurns] = useState([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [turns, status]);

  const startDebate = (topic, field) => {
    setPhase("running");
    setStatus("Connecting...");
    setTurns([]);
    setProfessors([]);

    fetch("/api/debate/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, field }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`API error: ${res.status} ${res.statusText}`);
        }
        if (!res.body) {
          throw new Error("Unable to read response body");
        }
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        const read = ({ done, value }) => {
          if (done) {
            console.log("[Debate] Stream ended");
            setPhase("done");
            return;
          }
          buffer += decoder.decode(value, { stream: true });
          const parts = buffer.split("\n\n");
          buffer = parts.pop() || "";

          for (const part of parts) {
            if (!part.trim()) continue;
            const eM = part.match(/^event:\s*(.+)$/m);
            const dM = part.match(/^data:\s*(.+)$/m);
            if (!eM || !dM) {
              console.warn(
                "[SSE] Invalid message format:",
                part.substring(0, 50),
              );
              continue;
            }
            try {
              handleEvent(eM[1].trim(), JSON.parse(dM[1]));
              console.log("[SSE]", eM[1].trim());
            } catch (err) {
              console.error(
                "[SSE] Parse error:",
                err.message,
                "Event:",
                eM[1],
                "Data:",
                dM[1].substring(0, 50),
              );
            }
          }
          reader
            .read()
            .then(read)
            .catch((err) => {
              console.error("[Reader error]", err);
              setStatus("Error: connection lost - " + err.message);
              setPhase("done");
            });
        };
        reader
          .read()
          .then(read)
          .catch((err) => {
            console.error("[Initial read error]", err);
            setStatus("Error: unable to read stream - " + err.message);
            setPhase("done");
          });
      })
      .catch((err) => {
        console.error("[Fetch error]", err);
        setStatus("Error: " + err.message);
        setPhase("setup");
      });
  };

  const handleEvent = (event, data) => {
    if (event === "status") {
      setStatus(data.message);
      return;
    }
    if (event === "professors") {
      setProfessors(data.professors);
      return;
    }
    if (event === "round")
      return setTurns((t) => [
        ...t,
        { type: "round", round: data.round, id: Date.now() },
      ]);
    if (event === "moderator")
      return setTurns((t) => [
        ...t,
        {
          type: "moderator",
          label: data.label,
          content: data.content,
          id: Date.now(),
        },
      ]);
    if (event === "speaker_start")
      return setTurns((t) => [
        ...t,
        {
          type: "professor",
          key: data.key,
          name: data.name,
          role: data.role,
          turn: data.turn,
          content: "",
          streaming: true,
          id: `${data.turn}-${data.key}`,
        },
      ]);
    if (event === "chunk")
      return setTurns((t) => {
        const last = t[t.length - 1];
        if (!last?.streaming) return t;
        return [
          ...t.slice(0, -1),
          { ...last, content: last.content + data.text },
        ];
      });
    if (event === "speaker_end")
      return setTurns((t) => {
        const idx = t.findIndex((x) => x.id === `${data.turn}-${data.key}`);
        if (idx === -1) return t;
        const u = [...t];
        u[idx] = { ...u[idx], streaming: false, fact_tags: data.fact_tags };
        return u;
      });
    if (event === "final")
      return setTurns((t) => [
        ...t,
        { type: "final", content: data.content, id: "final" },
      ]);
    if (event === "research_kit")
      return setTurns((t) => [
        ...t,
        {
          type: "research_kit",
          outline: data.outline,
          key_findings: data.key_findings,
          open_questions: data.open_questions,
          recommendations: data.recommendations,
          id: "research_kit",
        },
      ]);
    if (event === "saved") setStatus("✓ Saved: " + data.filename);
    if (event === "error") {
      setStatus("Error: " + data.message);
      setPhase("done");
    }
  };

  if (phase === "setup") return <SetupForm onStart={startDebate} />;

  return (
    <div style={s.arena}>
      <aside style={s.sidebar}>
        <div style={s.sideTitle}>Professors</div>
        {professors.map((p, i) => (
          <ProfessorCard key={p.key} prof={p} color={PROF_COLORS[i]} />
        ))}
        {phase === "done" && (
          <button style={s.newBtn} onClick={() => setPhase("setup")}>
            ← New debate
          </button>
        )}
      </aside>
      <main style={s.feed}>
        <div style={s.statusBar}>{status}</div>
        {turns.map((turn) => (
          <TurnBubble key={turn.id} turn={turn} professors={professors} />
        ))}
        <div ref={bottomRef} />
      </main>
    </div>
  );
}

// ── Styles ────────────────────────────────────────────────────────────────────
const s = {
  setupOuter: { maxWidth: 680, margin: "60px auto", padding: "0 20px" },
  logo: {
    fontSize: 26,
    fontWeight: 700,
    marginBottom: 6,
    background: "linear-gradient(135deg,#4fc3f7,#ce93d8)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  subtitle: { color: "#777", marginBottom: 24, fontSize: 14 },
  tabs: { display: "flex", gap: 6, marginBottom: 20 },
  tab: {
    background: "transparent",
    border: "1px solid #2e3248",
    borderRadius: 6,
    padding: "6px 14px",
    color: "#888",
    cursor: "pointer",
    fontSize: 13,
  },
  tabActive: {
    background: "#1a1f35",
    color: "#e8e8e8",
    borderColor: "#4a4f6a",
  },
  form: { display: "flex", flexDirection: "column", gap: 10 },
  label: { fontSize: 12, color: "#888" },
  input: {
    background: "#1a1d27",
    border: "1px solid #2e3248",
    borderRadius: 8,
    padding: "9px 13px",
    color: "#e8e8e8",
    fontSize: 14,
    outline: "none",
    width: "100%",
  },
  btn: {
    background: "linear-gradient(135deg,#4fc3f7,#7c4dff)",
    border: "none",
    borderRadius: 8,
    padding: "11px 20px",
    color: "#fff",
    fontSize: 14,
    fontWeight: 600,
    cursor: "pointer",
    marginTop: 6,
  },

  libWrap: { display: "flex", flexDirection: "column", gap: 2 },
  libTitle: {
    fontSize: 11,
    color: "#666",
    fontWeight: 600,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    marginBottom: 10,
  },
  libCat: {
    display: "flex",
    justifyContent: "space-between",
    padding: "8px 10px",
    background: "#1a1d27",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 13,
    color: "#ccc",
    marginBottom: 2,
  },
  libChevron: { color: "#666" },
  libTopic: {
    padding: "7px 14px",
    fontSize: 12,
    color: "#999",
    cursor: "pointer",
    borderLeft: "2px solid #2e3248",
    marginLeft: 8,
    marginBottom: 2,
    lineHeight: 1.5,
    ":hover": { color: "#4fc3f7" },
  },

  histWrap: { display: "flex", flexDirection: "column", gap: 8 },
  histEmpty: { color: "#666", fontSize: 13, padding: "20px 0" },
  histCard: {
    background: "#1a1d27",
    borderRadius: 8,
    padding: "10px 14px",
    cursor: "pointer",
    border: "1px solid #2e3248",
  },
  histTopic: { fontSize: 13, color: "#ccc", marginBottom: 4, lineHeight: 1.4 },
  histMeta: { fontSize: 11, color: "#666" },

  transcriptWrap: { maxWidth: 800, margin: "40px auto", padding: "0 20px" },
  transcriptTitle: {
    fontSize: 18,
    fontWeight: 600,
    color: "#e8e8e8",
    margin: "12px 0 6px",
  },
  transcriptMeta: { fontSize: 12, color: "#666", marginBottom: 20 },
  transcriptContent: {
    fontSize: 13,
    color: "#ccc",
    lineHeight: 1.7,
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    background: "#1a1d27",
    borderRadius: 8,
    padding: 20,
  },
  backBtn: {
    background: "transparent",
    border: "1px solid #2e3248",
    borderRadius: 6,
    padding: "6px 14px",
    color: "#888",
    cursor: "pointer",
    fontSize: 13,
  },

  arena: { display: "flex", height: "100vh", overflow: "hidden" },
  sidebar: {
    width: 260,
    padding: 16,
    borderRight: "1px solid #2e3248",
    overflowY: "auto",
    flexShrink: 0,
    display: "flex",
    flexDirection: "column",
    gap: 4,
  },
  sideTitle: {
    fontSize: 11,
    fontWeight: 600,
    color: "#666",
    letterSpacing: "0.1em",
    textTransform: "uppercase",
    marginBottom: 8,
  },
  profCard: {
    display: "flex",
    gap: 8,
    padding: "8px 6px",
    borderBottom: "1px solid #1e2235",
    borderLeft: "3px solid",
    paddingLeft: 8,
  },
  profAvatar: {
    width: 30,
    height: 30,
    borderRadius: 7,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 14,
    flexShrink: 0,
  },
  profName: { fontSize: 12, fontWeight: 600, marginBottom: 1 },
  profUni: { fontSize: 10, color: "#555", marginBottom: 1 },
  profRole: { fontSize: 10, color: "#777" },
  profStance: { fontSize: 10, color: "#555", marginTop: 2, lineHeight: 1.4 },
  newBtn: {
    marginTop: "auto",
    background: "transparent",
    border: "1px solid #2e3248",
    borderRadius: 6,
    padding: "8px",
    color: "#888",
    cursor: "pointer",
    fontSize: 12,
  },

  feed: {
    flex: 1,
    overflowY: "auto",
    padding: "16px 24px",
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  statusBar: { fontSize: 12, color: "#555", padding: "4px 0" },
  roundDivider: {
    textAlign: "center",
    color: "#444",
    fontSize: 11,
    padding: "6px 0",
    letterSpacing: "0.1em",
  },
  modBubble: {
    background: "#1a1f35",
    borderLeft: "3px solid #7c4dff",
    borderRadius: "0 8px 8px 0",
    padding: "10px 14px",
  },
  modLabel: {
    fontSize: 11,
    color: "#7c4dff",
    fontWeight: 600,
    marginBottom: 5,
  },
  modContent: { fontSize: 13, color: "#bbb", lineHeight: 1.6 },
  turnWrap: { borderLeft: "3px solid", paddingLeft: 14, paddingBottom: 4 },
  turnHeader: {
    display: "flex",
    alignItems: "center",
    gap: 8,
    marginBottom: 5,
  },
  turnName: { fontSize: 13, fontWeight: 600 },
  turnRole: { fontSize: 11, color: "#666" },
  turnNum: { fontSize: 11, color: "#444", marginLeft: "auto" },
  turnContent: { fontSize: 13, lineHeight: 1.7, color: "#ddd" },
  cursor: { animation: "blink 1s infinite" },
  factWrap: { marginTop: 8, display: "flex", flexDirection: "column", gap: 3 },
  factRow: {
    display: "flex",
    alignItems: "baseline",
    gap: 5,
    flexWrap: "wrap",
  },
  factBadge: {
    fontSize: 10,
    fontWeight: 600,
    padding: "1px 5px",
    border: "1px solid",
    borderRadius: 3,
    flexShrink: 0,
  },
  factClaim: { fontSize: 11, color: "#888" },
  factReason: { fontSize: 11, color: "#666", fontStyle: "italic" },
  factSource: { fontSize: 11, color: "#4fc3f7", marginLeft: 6, width: "100%" },
  finalWrap: {
    background: "#0d1b14",
    border: "1px solid #1e3a2a",
    borderRadius: 10,
    padding: "14px 18px",
    marginTop: 6,
  },
  finalTitle: {
    fontSize: 13,
    fontWeight: 700,
    color: "#66bb6a",
    marginBottom: 10,
  },
  finalSection: {
    fontSize: 12,
    color: "#81c784",
    fontWeight: 600,
    marginTop: 8,
  },
  finalBullet: { fontSize: 12, color: "#bbb", paddingLeft: 10, marginTop: 3 },
  finalLine: { fontSize: 12, color: "#999", marginTop: 2 },

  // Research Kit styles
  researchWrap: {
    background: "#0a1929",
    border: "1px solid #1565a0",
    borderRadius: 10,
    padding: "16px 18px",
    marginTop: 12,
  },
  researchTitle: {
    fontSize: 16,
    fontWeight: 700,
    color: "#42a5f5",
    marginBottom: 16,
  },
  researchSection: {
    marginBottom: 18,
  },
  researchHeading: {
    fontSize: 12,
    fontWeight: 700,
    color: "#64b5f6",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    marginBottom: 8,
  },
  researchContent: {
    background: "#1a2332",
    color: "#b3e5fc",
    padding: 12,
    borderRadius: 6,
    fontSize: 11,
    lineHeight: 1.5,
    overflow: "auto",
    maxHeight: 300,
    border: "1px solid #0d47a1",
  },
  findingItem: {
    background: "#1a2332",
    borderLeft: "3px solid #42a5f5",
    padding: "8px 12px",
    marginBottom: 8,
    borderRadius: 4,
  },
  findingText: {
    fontSize: 12,
    color: "#b3e5fc",
    marginBottom: 4,
  },
  findingEvidence: {
    fontSize: 11,
    color: "#81d4fa",
    marginBottom: 2,
  },
  findingImpact: {
    fontSize: 11,
    color: "#4fc3f7",
  },
};
