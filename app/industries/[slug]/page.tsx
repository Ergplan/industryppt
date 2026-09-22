import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Deck } from "@/components/deck/Deck";
import { deckSlugs, getDeck } from "@/lib/decks";

type Props = { params: Promise<{ slug: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return deckSlugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const deck = getDeck((await params).slug);
  if (!deck) return {};
  return { title: deck.meta.title, description: deck.meta.description, openGraph: { title: deck.meta.title, description: deck.meta.description } };
}

export default async function IndustryPage({ params }: Props) {
  const deck = getDeck((await params).slug);
  if (!deck) notFound();
  return <Deck deck={deck} />;
}
