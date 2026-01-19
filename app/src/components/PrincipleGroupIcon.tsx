// app/src/components/PrincipleGroupIcon.tsx
import type { FC, ReactElement } from 'react';

interface PrincipleGroupIconProps {
  groupId: string;
  color: string;
  className?: string;
}

export const PrincipleGroupIcon: FC<PrincipleGroupIconProps> = ({
  groupId,
  color,
  className = 'w-10 h-10',
}) => {
  const icons: Record<string, ReactElement> = {
    protection: (
      // Shield icon
      <svg
        viewBox="0 0 48 48"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M24 4L6 12v12c0 11 8 18 18 20 10-2 18-9 18-20V12L24 4z"
          fill={color}
          opacity="0.2"
          stroke={color}
          strokeWidth="2"
        />
        <path
          d="M16 24l6 6 10-12"
          stroke={color}
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
    'lab-to-org': (
      // Connection/handoff icon
      <svg
        viewBox="0 0 48 48"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="12" cy="24" r="8" fill={color} opacity="0.3" stroke={color} strokeWidth="2" />
        <circle cx="36" cy="24" r="8" fill={color} opacity="0.3" stroke={color} strokeWidth="2" />
        <path d="M20 24h8" stroke={color} strokeWidth="2" />
        <path
          d="M25 20l4 4-4 4"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
    incentives: (
      // Target/measurement icon
      <svg
        viewBox="0 0 48 48"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="24" cy="24" r="16" stroke={color} strokeWidth="2" opacity="0.3" />
        <circle cx="24" cy="24" r="10" stroke={color} strokeWidth="2" opacity="0.5" />
        <circle cx="24" cy="24" r="4" fill={color} />
      </svg>
    ),
    culture: (
      // People/community icon
      <svg
        viewBox="0 0 48 48"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="24" cy="14" r="6" fill={color} opacity="0.7" />
        <circle cx="12" cy="20" r="5" fill={color} opacity="0.5" />
        <circle cx="36" cy="20" r="5" fill={color} opacity="0.5" />
        <path
          d="M8 40c0-8 7-12 16-12s16 4 16 12"
          stroke={color}
          strokeWidth="2"
          fill={color}
          opacity="0.2"
        />
      </svg>
    ),
    resources: (
      // Talent/people with star icon
      <svg
        viewBox="0 0 48 48"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="20" cy="18" r="8" fill={color} opacity="0.3" stroke={color} strokeWidth="2" />
        <path d="M6 42c0-8 6-14 14-14s14 6 14 14" stroke={color} strokeWidth="2" />
        <path d="M36 12l2 4 4 1-3 3 1 4-4-2-4 2 1-4-3-3 4-1z" fill={color} />
      </svg>
    ),
    speed: (
      // Fast forward / clock icon
      <svg
        viewBox="0 0 48 48"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="24" cy="24" r="16" stroke={color} strokeWidth="2" opacity="0.3" />
        <path
          d="M24 12v12l8 4"
          stroke={color}
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M36 18l6 6-6 6"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  };

  return (
    icons[groupId] || (
      <svg
        viewBox="0 0 48 48"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="24" cy="24" r="16" stroke={color} strokeWidth="2" />
      </svg>
    )
  );
};
