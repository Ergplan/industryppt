"use client";
import { useEffect, useRef } from "react";
import { initDeckInteractive } from "@/lib/deck-interactive";
import { enhance } from "@/lib/jwchart";

/** Turns the deck's charts into hover/tap readouts after hydration.
 *  The wiring itself lives in lib/deck-interactive.js so the standalone HTML
 *  exports can inline the same file — see tools/generator/build.py. */
export function DeckInteractive() {
  const anchor = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    const deck = anchor.current?.closest(".jw-deck");
    if (!deck) return;
    const offDeck = initDeckInteractive(deck);
    const offCharts = enhance(deck);
    return () => { offCharts(); offDeck(); };
  }, []);
  return <span ref={anchor} hidden aria-hidden="true" />;
}
