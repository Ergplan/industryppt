import Link from "next/link";
import type { Metadata } from "next";
import { decks } from "@/lib/decks";

export const metadata: Metadata = {
  title: "Industries · jouleWise decarbonisation stack",
  description: "Green power, green heat and the data that proves both — by industry.",
};

export default function IndustriesIndex() {
  return (
    <div className="jw-deck">
      <main>
        <section className="pg cover">
          <div className="eb">Industries <i>/ power · heat · proof</i></div>
          <h1>One stack.<br /><span className="g">Every industry.</span></h1>
          <p className="lede">Green power, green heat, ergOS and esgOS from one provider — mapped to the way each industry actually uses energy.</p>
          <nav className="jw-index" aria-label="Industry decks">
            {decks.map((d) => (
              <Link key={d.slug} href={`/industries/${d.slug}`}>
                <b>{d.short}</b>
                <span>{d.cover.sub}</span>
              </Link>
            ))}
          </nav>
        </section>
      </main>
    </div>
  );
}
