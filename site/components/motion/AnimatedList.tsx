"use client";

import { AnimatePresence, motion } from "framer-motion";
import type { ReactNode } from "react";

export function AnimatedList({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <AnimatePresence mode="popLayout">
      <div className={className}>{children}</div>
    </AnimatePresence>
  );
}

export function AnimatedListItem({
  children,
  itemKey,
}: {
  children: ReactNode;
  itemKey: string;
}) {
  return (
    <motion.div
      key={itemKey}
      layout
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.97 }}
      transition={{ duration: 0.2, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
