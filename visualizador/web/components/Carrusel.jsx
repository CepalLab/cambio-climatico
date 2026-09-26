"use client";
import { useState } from "react";
import DocCard from "./DocCard";

export default function Carrusel({ docs }) {
  const [ini, setIni] = useState(0);
  const total = docs.length;
  const visibles = docs.slice(ini, ini + 3);
  const pag = Math.floor(ini / 3) + 1;
  const npag = Math.ceil(total / 3);
  const avanzar = (d) => setIni((i) => (i + d + total) % total);

  return (
    <div>
      <div className="carrusel">
        {visibles.map((doc) => (
          <DocCard key={doc.id} doc={doc} />
        ))}
      </div>
      <div className="controles">
        <button onClick={() => avanzar(-1)} aria-label="Anterior">←</button>
        <span className="contador">
          {String(pag).padStart(2, "0")} / {String(npag).padStart(2, "0")}
        </span>
        <button onClick={() => avanzar(1)} aria-label="Siguiente">→</button>
      </div>
    </div>
  );
}
