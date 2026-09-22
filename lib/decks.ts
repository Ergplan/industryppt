import automotive from "@/content/decks/automotive.json";
import pharma from "@/content/decks/pharma.json";
import textile from "@/content/decks/textile.json";
import hotels from "@/content/decks/hotels.json";
import beverages from "@/content/decks/beverages.json";
import type { DeckData } from "./types";

/** Order here is the order industries appear on the index page. */
export const decks: DeckData[] = [automotive, pharma, textile, hotels, beverages] as DeckData[];

export const deckSlugs = decks.map((d) => d.slug);

export function getDeck(slug: string): DeckData | undefined {
  return decks.find((d) => d.slug === slug);
}
