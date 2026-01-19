// app/src/services/ai.ts

import { getConfig } from './config';
import type { Case, DesignPrinciple } from '../types/library';

interface AIResponse {
  answer: string;
  source: 'stored' | 'reasoning' | 'web-search';
  shouldPersist: boolean;
}

/**
 * 3-tier knowledge system:
 * 1. Check stored data (conversations, extendedContent)
 * 2. Use AI reasoning with context
 * 3. Fall back to web search if needed
 */
export async function askAboutCase(caseStudy: Case, question: string): Promise<AIResponse> {
  // Tier 1: Check if we have a stored answer
  const existingConversation = caseStudy.conversations.find(
    (c) => c.question.toLowerCase() === question.toLowerCase()
  );
  if (existingConversation) {
    return {
      answer: existingConversation.answer,
      source: 'stored',
      shouldPersist: false,
    };
  }

  // Check extendedContent for relevant info
  const relevantExtended = Object.entries(caseStudy.extendedContent)
    .filter(([key]) => key.toLowerCase().includes(question.toLowerCase().split(' ')[0]))
    .map(([, value]) => value)
    .join('\n');

  // Tier 2: AI reasoning with context
  const config = getConfig();
  if (!config.anthropicApiKey) {
    throw new Error('Anthropic API key not configured. Please set it in Settings.');
  }

  const context = buildCaseContext(caseStudy, relevantExtended);
  const aiResponse = await callClaude(config.anthropicApiKey, context, question);

  // Check if AI indicates it needs more information
  if (aiResponse.needsWebSearch && config.webSearchApiKey && config.webSearchApiUrl) {
    // Tier 3: Web search
    const searchResults = await performWebSearch(
      config.webSearchApiKey,
      config.webSearchApiUrl,
      `${caseStudy.company} AI transformation ${question}`
    );

    const enrichedResponse = await callClaude(
      config.anthropicApiKey,
      context + '\n\nAdditional research:\n' + searchResults,
      question
    );

    return {
      answer: enrichedResponse.answer,
      source: 'web-search',
      shouldPersist: true,
    };
  }

  return {
    answer: aiResponse.answer,
    source: 'reasoning',
    shouldPersist: aiResponse.isNewInfo,
  };
}

export async function askAboutPrinciple(
  principle: DesignPrinciple,
  question: string
): Promise<AIResponse> {
  // Similar implementation for principles
  const existingConversation = principle.conversations.find(
    (c) => c.question.toLowerCase() === question.toLowerCase()
  );
  if (existingConversation) {
    return {
      answer: existingConversation.answer,
      source: 'stored',
      shouldPersist: false,
    };
  }

  const config = getConfig();
  if (!config.anthropicApiKey) {
    throw new Error('Anthropic API key not configured. Please set it in Settings.');
  }

  const context = buildPrincipleContext(principle);
  const aiResponse = await callClaude(config.anthropicApiKey, context, question);

  if (aiResponse.needsWebSearch && config.webSearchApiKey && config.webSearchApiUrl) {
    const searchResults = await performWebSearch(
      config.webSearchApiKey,
      config.webSearchApiUrl,
      `${principle.title} organizational design ${question}`
    );

    const enrichedResponse = await callClaude(
      config.anthropicApiKey,
      context + '\n\nAdditional research:\n' + searchResults,
      question
    );

    return {
      answer: enrichedResponse.answer,
      source: 'web-search',
      shouldPersist: true,
    };
  }

  return {
    answer: aiResponse.answer,
    source: 'reasoning',
    shouldPersist: aiResponse.isNewInfo,
  };
}

function buildCaseContext(caseStudy: Case, extendedContent: string): string {
  return `
You are an expert on organizational AI transformation. You have deep knowledge about the following case study:

**Company:** ${caseStudy.company}
**Model:** ${caseStudy.title}

**What It Is:**
${caseStudy.content.whatItIs}

**How It Works:**
${caseStudy.content.howItWorks.map((h) => `- ${h}`).join('\n')}

**Core Insight:**
${caseStudy.content.coreInsight}

${caseStudy.content.keyMetrics ? `**Key Metrics:**\n${caseStudy.content.keyMetrics}` : ''}

**Sources:**
${caseStudy.content.sources.join(', ')}

${extendedContent ? `**Additional Context:**\n${extendedContent}` : ''}

Previous conversations about this case:
${caseStudy.conversations.map((c) => `Q: ${c.question}\nA: ${c.answer}`).join('\n\n')}
`.trim();
}

function buildPrincipleContext(principle: DesignPrinciple): string {
  return `
You are an expert on organizational design principles for AI transformation. You have deep knowledge about the following principle:

**Principle:** ${principle.title}

**Core Insight:**
${principle.insight}

**Manifestations:**
${principle.manifestations.map((m) => `- ${m}`).join('\n')}

**Diagnostic Test:**
${principle.test}

Previous conversations about this principle:
${principle.conversations.map((c) => `Q: ${c.question}\nA: ${c.answer}`).join('\n\n')}
`.trim();
}

interface ClaudeResponse {
  answer: string;
  needsWebSearch: boolean;
  isNewInfo: boolean;
}

async function callClaude(apiKey: string, context: string, question: string): Promise<ClaudeResponse> {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      system: `${context}

You are answering questions about this organizational case/principle. Be concise but thorough.

If you don't have enough information to answer the question well, respond with exactly:
"[NEEDS_RESEARCH] I need more current information to answer this accurately."

If you're providing information that goes beyond what's in the context (new insights, connections), start your response with "[NEW_INFO]" (this will be stripped from the final answer).

Otherwise, provide a helpful, specific answer based on the context provided.`,
      messages: [
        {
          role: 'user',
          content: question,
        },
      ],
    }),
  });

  if (!response.ok) {
    throw new Error(`Claude API error: ${response.statusText}`);
  }

  const data = await response.json();
  const content = data.content[0].text;

  if (content.startsWith('[NEEDS_RESEARCH]')) {
    return {
      answer: content.replace('[NEEDS_RESEARCH] ', ''),
      needsWebSearch: true,
      isNewInfo: false,
    };
  }

  if (content.startsWith('[NEW_INFO]')) {
    return {
      answer: content.replace('[NEW_INFO] ', ''),
      needsWebSearch: false,
      isNewInfo: true,
    };
  }

  return {
    answer: content,
    needsWebSearch: false,
    isNewInfo: false,
  };
}

async function performWebSearch(apiKey: string, apiUrl: string, query: string): Promise<string> {
  // This is a placeholder - the actual implementation depends on the user's web search API
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error(`Web search error: ${response.statusText}`);
  }

  const data = await response.json();
  // Format depends on the specific API - this is a generic handler
  return typeof data.results === 'string' ? data.results : JSON.stringify(data.results, null, 2);
}
