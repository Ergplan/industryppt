"use client";
import { useEffect, useRef, useState } from "react";

/** Sticky top bar with scroll progress and current page number. Optional — omit if the site header already covers it. */
export function DeckBar({ short, total }: { short: string; total: number }) {
  const prog = useRef<HTMLDivElement>(null);
  const [cur, setCur] = useState(0);
  useEffect(() => {
    const root = prog.current?.closest(".jw-deck");
    const pages = root ? Array.from(root.querySelectorAll<HTMLElement>(".pg")) : [];
    const onScroll = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      if (prog.current) prog.current.style.width = `${max > 0 ? (100 * h.scrollTop) / max : 0}%`;
      let k = 0;
      pages.forEach((p, i) => { if (p.getBoundingClientRect().top < 120) k = i; });
      setCur(k);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  const p2 = (n: number) => String(n).padStart(2, "0");
  return (
    <header className="bar">
      <div className="bar-in">
        <span className="logo"><span className="j">joule</span><span className="w">Wise</span></span>
        <div className="bar-r">
          <span className="x">Decarbonisation stack · </span><b>{short}</b> · <span>{p2(cur)}</span>/{p2(total)}
        </div>
      </div>
      <div className="prog" ref={prog} />
    </header>
  );
}
