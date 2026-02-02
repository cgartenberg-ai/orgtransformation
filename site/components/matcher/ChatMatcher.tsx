"use client";

import { useState, useRef, useEffect, useCallback } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const STORAGE_KEY = "afg-chat-messages";

const WELCOME_MESSAGE =
  "Tell me about your organization — what industry are you in, how large is the organization, and what's driving your interest in AI organization? I'll help you find the structural species that fits your situation.";

function loadMessages(): Message[] {
  if (typeof window === "undefined") return [{ role: "assistant", content: WELCOME_MESSAGE }];
  try {
    const stored = sessionStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored) as Message[];
      if (parsed.length > 0) return parsed;
    }
  } catch {
    // ignore
  }
  return [{ role: "assistant", content: WELCOME_MESSAGE }];
}

export function ChatMatcher() {
  const [messages, setMessages] = useState<Message[]>(() => loadMessages());
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Persist messages to sessionStorage whenever they change
  const persistMessages = useCallback((msgs: Message[]) => {
    try {
      // Only persist non-empty assistant messages (skip mid-stream empty ones)
      const toStore = msgs.filter((m) => m.content.length > 0);
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(toStore));
    } catch {
      // ignore quota errors
    }
  }, []);

  useEffect(() => {
    if (!isStreaming) {
      persistMessages(messages);
    }
  }, [messages, isStreaming, persistMessages]);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || isStreaming) return;

    const userMessage: Message = { role: "user", content: text };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setIsStreaming(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages.filter((m) =>
            // Don't send welcome message to API
            m !== updatedMessages[0] || m.role !== "assistant"
          ),
        }),
      });

      if (!res.ok) {
        throw new Error(`API error: ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No reader");

      const decoder = new TextDecoder();
      let assistantText = "";

      // Add empty assistant message that we'll stream into
      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        assistantText += decoder.decode(value, { stream: true });
        const currentText = assistantText;
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: "assistant",
            content: currentText,
          };
          return updated;
        });
      }
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I'm having trouble connecting right now. Please check that the API key is configured and try again.",
        },
      ]);
    } finally {
      setIsStreaming(false);
      inputRef.current?.focus();
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  }

  function handleReset() {
    setMessages([{ role: "assistant", content: WELCOME_MESSAGE }]);
    sessionStorage.removeItem(STORAGE_KEY);
  }

  const hasConversation = messages.length > 1;

  return (
    <div className="flex h-[600px] flex-col rounded-xl border border-sage-200 bg-cream-50 shadow-sm">
      {/* Messages */}
      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto p-5">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-forest text-cream"
                  : "border border-sage-200 bg-white text-charcoal-700"
              }`}
            >
              <MessageContent content={msg.content} />
            </div>
          </div>
        ))}
        {isStreaming && messages[messages.length - 1]?.content === "" && (
          <div className="flex justify-start">
            <div className="rounded-2xl border border-sage-200 bg-white px-4 py-3">
              <span className="inline-flex gap-1">
                <span className="h-2 w-2 animate-bounce rounded-full bg-sage-400" style={{ animationDelay: "0ms" }} />
                <span className="h-2 w-2 animate-bounce rounded-full bg-sage-400" style={{ animationDelay: "150ms" }} />
                <span className="h-2 w-2 animate-bounce rounded-full bg-sage-400" style={{ animationDelay: "300ms" }} />
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-sage-200 p-4">
        <div className="flex gap-3">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your organization..."
            rows={1}
            className="flex-1 resize-none rounded-lg border border-sage-200 bg-white px-4 py-2.5 text-sm text-charcoal-700 placeholder:text-charcoal-300 focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
            disabled={isStreaming}
          />
          <button
            type="submit"
            disabled={isStreaming || !input.trim()}
            className="shrink-0 rounded-lg bg-forest px-5 py-2.5 text-sm font-semibold text-cream transition-colors hover:bg-forest-600 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
        {hasConversation && (
          <button
            type="button"
            onClick={handleReset}
            className="mt-2 text-xs text-charcoal-400 underline hover:text-forest"
          >
            Start new conversation
          </button>
        )}
      </form>
    </div>
  );
}

/** Render markdown links as clickable <a> tags */
function MessageContent({ content }: { content: string }) {
  if (!content) return null;

  // Split on markdown links: [text](url)
  const parts = content.split(/(\[[^\]]+\]\([^)]+\))/g);

  return (
    <>
      {parts.map((part, i) => {
        const linkMatch = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
        if (linkMatch) {
          return (
            <a
              key={i}
              href={linkMatch[2]}
              className="font-medium underline decoration-1 underline-offset-2 hover:opacity-80"
            >
              {linkMatch[1]}
            </a>
          );
        }
        // Handle line breaks
        return part.split("\n").map((line, j, arr) => (
          <span key={`${i}-${j}`}>
            {line}
            {j < arr.length - 1 && <br />}
          </span>
        ));
      })}
    </>
  );
}
