// app/src/components/DiagramIcon.tsx
import type { FC, ReactElement } from 'react';

interface DiagramIconProps {
  templateId: string;
  className?: string;
}

export const DiagramIcon: FC<DiagramIconProps> = ({ templateId, className = 'w-16 h-16' }) => {
  const diagrams: Record<string, ReactElement> = {
    'centralized-lab': (
      // Single large circle (lab) separate from grid of small circles (operations)
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="32" r="14" fill="#6366f1" opacity="0.8" />
        <rect x="40" y="16" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="16" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="40" y="24" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="24" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="40" y="32" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="32" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="40" y="40" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="40" width="6" height="6" rx="1" fill="#94a3b8" />
        <line x1="34" y1="32" x2="38" y2="32" stroke="#cbd5e1" strokeWidth="2" strokeDasharray="2 2" />
      </svg>
    ),
    'distributed-hubs': (
      // Multiple medium circles spread out, connected by lines
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="48" cy="16" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="16" cy="48" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="48" cy="48" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="32" cy="32" r="6" fill="#94a3b8" opacity="0.5" />
        <line x1="24" y1="16" x2="40" y2="16" stroke="#cbd5e1" strokeWidth="1.5" />
        <line x1="16" y1="24" x2="16" y2="40" stroke="#cbd5e1" strokeWidth="1.5" />
        <line x1="48" y1="24" x2="48" y2="40" stroke="#cbd5e1" strokeWidth="1.5" />
        <line x1="24" y1="48" x2="40" y2="48" stroke="#cbd5e1" strokeWidth="1.5" />
      </svg>
    ),
    'embedded-universal': (
      // Grid of identical circles all with AI indicator
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="32" cy="16" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="48" cy="16" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="16" cy="32" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="32" cy="32" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="48" cy="32" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="16" cy="48" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="32" cy="48" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="48" cy="48" r="6" fill="#6366f1" opacity="0.6" />
        <text x="16" y="19" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="32" y="19" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="48" y="19" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="16" y="35" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="32" y="35" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="48" y="35" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="16" y="51" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="32" y="51" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="48" y="51" textAnchor="middle" fontSize="8" fill="white">AI</text>
      </svg>
    ),
    'center-of-excellence': (
      // Central circle with spokes radiating to outer circles
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="32" cy="32" r="10" fill="#6366f1" opacity="0.8" />
        <circle cx="32" cy="8" r="5" fill="#94a3b8" />
        <circle cx="56" cy="32" r="5" fill="#94a3b8" />
        <circle cx="32" cy="56" r="5" fill="#94a3b8" />
        <circle cx="8" cy="32" r="5" fill="#94a3b8" />
        <line x1="32" y1="22" x2="32" y2="13" stroke="#6366f1" strokeWidth="2" />
        <line x1="42" y1="32" x2="51" y2="32" stroke="#6366f1" strokeWidth="2" />
        <line x1="32" y1="42" x2="32" y2="51" stroke="#6366f1" strokeWidth="2" />
        <line x1="22" y1="32" x2="13" y2="32" stroke="#6366f1" strokeWidth="2" />
      </svg>
    ),
    'product-as-lab': (
      // Product box with arrows cycling back (data flywheel)
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="18" y="22" width="28" height="20" rx="2" fill="#6366f1" opacity="0.7" />
        <text x="32" y="35" textAnchor="middle" fontSize="8" fill="white">PRODUCT</text>
        <path d="M32 8 L40 16 L36 16 L36 20 L28 20 L28 16 L24 16 Z" fill="#10b981" />
        <path d="M32 56 L24 48 L28 48 L28 44 L36 44 L36 48 L40 48 Z" fill="#10b981" />
        <path d="M8 32 L16 24 L16 28 L18 28 L18 36 L16 36 L16 40 Z" fill="#94a3b8" opacity="0.6" />
        <path d="M56 32 L48 40 L48 36 L46 36 L46 28 L48 28 L48 24 Z" fill="#94a3b8" opacity="0.6" />
      </svg>
    ),
    'hybrid-labs-core': (
      // Two connected circles - one labeled Labs, one Core
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="32" r="12" fill="#6366f1" opacity="0.8" />
        <circle cx="44" cy="32" r="12" fill="#10b981" opacity="0.7" />
        <ellipse cx="32" cy="32" rx="4" ry="8" fill="#6366f1" opacity="0.3" />
        <text x="20" y="35" textAnchor="middle" fontSize="6" fill="white">Labs</text>
        <text x="44" y="35" textAnchor="middle" fontSize="6" fill="white">Core</text>
      </svg>
    ),
    'tight-loop': (
      // Two boxes with circular arrows between them
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="6" y="22" width="20" height="20" rx="2" fill="#6366f1" opacity="0.7" />
        <rect x="38" y="22" width="20" height="20" rx="2" fill="#10b981" opacity="0.7" />
        <text x="16" y="35" textAnchor="middle" fontSize="5" fill="white">Predict</text>
        <text x="48" y="35" textAnchor="middle" fontSize="5" fill="white">Validate</text>
        <path d="M28 28 C32 24, 34 24, 36 28" stroke="#f59e0b" strokeWidth="2" fill="none" markerEnd="url(#arrowhead)" />
        <path d="M36 36 C34 40, 32 40, 28 36" stroke="#f59e0b" strokeWidth="2" fill="none" markerEnd="url(#arrowhead)" />
        <defs>
          <marker id="arrowhead" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
            <polygon points="0 0, 6 3, 0 6" fill="#f59e0b" />
          </marker>
        </defs>
      </svg>
    ),
    'external-acquisition': (
      // Arrow coming from outside into org boundary
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="24" y="12" width="32" height="40" rx="2" stroke="#94a3b8" strokeWidth="2" strokeDasharray="4 2" fill="none" />
        <circle cx="40" cy="32" r="10" fill="#6366f1" opacity="0.7" />
        <circle cx="10" cy="32" r="8" fill="#10b981" opacity="0.8" />
        <path d="M18 32 L22 32" stroke="#10b981" strokeWidth="3" />
        <polygon points="24,32 20,28 20,36" fill="#10b981" />
      </svg>
    ),
    'broad-deployment': (
      // Single source spreading to many targets simultaneously
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="32" r="8" fill="#6366f1" opacity="0.8" />
        <circle cx="44" cy="12" r="5" fill="#94a3b8" />
        <circle cx="52" cy="24" r="5" fill="#94a3b8" />
        <circle cx="56" cy="38" r="5" fill="#94a3b8" />
        <circle cx="52" cy="52" r="5" fill="#94a3b8" />
        <circle cx="40" cy="56" r="5" fill="#94a3b8" />
        <line x1="20" y1="28" x2="39" y2="14" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="30" x2="47" y2="24" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="32" x2="51" y2="38" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="34" x2="47" y2="50" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="36" x2="35" y2="54" stroke="#6366f1" strokeWidth="1.5" />
      </svg>
    ),
  };

  return diagrams[templateId] || (
    <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="8" y="8" width="48" height="48" rx="4" stroke="#94a3b8" strokeWidth="2" fill="none" />
      <text x="32" y="36" textAnchor="middle" fontSize="10" fill="#94a3b8">?</text>
    </svg>
  );
};
