# Ralnova Connect – Social-Media-Leitfaden

Gilt für jeden Wochenplan, ob von Hand oder automatisch erstellt. Vor jeder neuen Woche komplett lesen.

## Wer wir sind
Ralnova Connect (vormals G&R Werkbank Salzburg), gegründet von Noah und Lorenz. Zwei Angebote für Handwerksbetriebe in der Region Salzburg:
1. **Social Recruiting:** Fachkräfte über Meta-Anzeigen (Facebook/Instagram) gewinnen statt über Jobportale. Erfolgsbasiert: Der Betrieb zahlt erst, wenn jemand anfängt. Realistisch rund 60 Tage bis zur ersten Einstellung.
2. **Webseiten** für Handwerksbetriebe ohne zeitgemäße Seite.

## Rhythmus
- Jeden Tag 2 Posts auf Facebook + Instagram (über Metricool, Brand-ID 7406274, Zeitzone Europe/Berlin).
- **07:00 → Betriebe** (Inhaber, Sie-Form). **19:00 → Handwerker** (Gesellen/Fachkräfte, Du-Form).
- LinkedIn postet das Team selbst.

## Abwechslung (Pflicht)
- **Layouts:** klassik, block, zitat, liste, frage, rahmen. Nie dasselbe Layout zweimal hintereinander (über alle 14 Posts der Woche in zeitlicher Reihenfolge). Jedes Layout mindestens 2× pro Woche.
- **Farbwelten:** Betriebe: b-kohle, b-nacht, b-wald. Handwerker: h-creme, h-signal, h-sand. Innerhalb einer Zielgruppe nie zweimal hintereinander dieselbe Farbwelt.
- **liste** nur, wenn der Inhalt wirklich 3–5 Punkte hat (body = ein Punkt pro Zeile, ohne Nummern).
- **frage** für kurze, direkte Fragen (Überschrift max. ~60 Zeichen).
- **zitat** für typische Sätze/Einwände, die man in der Branche hört (z. B. „Wir finden eh niemanden.“). Nie als Kundenstimme oder Aussage einer echten Person ausgeben.
- **Themen:** Kein Thema und keine Überschrift wiederholen, die in den letzten 6 Wochen schon lief (alle Dateien in `posts/plan/` prüfen). Pro Woche mindestens 5 verschiedene Formate je Zielgruppe.
- **Hashtags:** 3–5, jedes Mal leicht variieren. Immer #salzburg.

## Themen-Pool

**Betriebe (Sie-Form)**
- Einwände aufgreifen: Mundpropaganda reicht · schon mit Agentur/Social Media probiert · Jobportal reicht · da melden sich nur Unqualifizierte · Markt ist leer · Fachkräfte sind nicht auf Instagram · keine Zeit für so was · wir haben eigene Personalabteilung
- Kosten des Nichtstuns: offene Stelle, geschobene Aufträge, überlastetes Team (immer als Rechenweg/Frage, nie mit erfundenen Zahlen)
- So arbeiten wir: Ablauf, Vorqualifizierung, erfolgsbasiert, ehrliche 60 Tage
- Was Bewerber wirklich sehen wollen: Team, Werkstatt, Projekte, Chef
- Warum gute Leute gehen / wie man sie hält (Wertschätzung, Abläufe, Werkzeug, Fahrzeiten)
- Gehalt und Anforderungen realistisch ansetzen (ohne konkrete Gehaltszahlen)
- Webseite: Wird Ihr Betrieb gegoogelt? Erster Eindruck, Handy-tauglich, Kundenstimmen zeigen, Anruf-Button
- Fragen an die Community (Kommentare anregen)

**Handwerker (Du-Form)**
- Wechselgründe: fehlende Wertschätzung, unbezahlte Fahrzeiten, kaputtes Werkzeug, kein Entwicklung
- Woran man einen guten Betrieb erkennt
- Einfacher Einstieg: kein Lebenslauf, kurze Nachricht, unverbindlich, diskret
- Gewerke direkt ansprechen: Tischler, Elektriker, Maler, Installateur, Zimmerer, Spengler, Fliesenleger, Dachdecker
- Gefühle des Alltags: Sonntagabend, Montagmorgen, Feierabend, Überstunden
- Weiterkommen: Verantwortung, Spezialisierung, Meister (ohne Versprechen)
- Fragen an die Community

## Harte Regeln
1. **Nichts erfinden:** keine Statistiken, Prozentzahlen, Gehälter, Kundenstimmen, Fallbeispiele, Erfolge oder Partnerbetriebe. Erlaubt sind nur Aussagen über unser eigenes Angebot (oben) und allgemeine Beobachtungen ohne Zahlen.
2. Keine konkreten offenen Stellen oder Arbeitgeber versprechen, die es nicht gibt („Wir suchen für Betriebe in Salzburg …“ ist ok, „Firma X sucht …“ nicht).
3. Keine Rechtsauskünfte (Kündigungsfristen, Arbeitsrecht).
4. Kein Werbesprech: nicht „revolutionär“, „einzigartig“, „ganzheitlich“, „maßgeschneidert“, „Synergie“. Keine Emojis im Bild, in der Caption höchstens 1–2.
5. Kein Konkurrent schlechtmachen, keine echten Firmennamen.
6. Sprache: klar, kurz, so wie Handwerker reden. Österreichisch-neutral.
7. Bildtexte kurz halten: Überschrift max. ~70 Zeichen, Fließtext max. ~200 Zeichen, Footer max. 2 kurze Zeilen. Das Render-Skript meldet „OVERFLOW“, wenn Text nicht passt → kürzen und neu rendern.
8. CTA Betriebe: „Jetzt Nachricht schreiben“ (oder ähnlich kurz). CTA Handwerker: „Schreib uns „JOB““ (oder ähnlich kurz).

## Ablauf für eine Woche (Mo–So)
1. `CONTENT.md` und die letzten 6 Pläne in `posts/plan/` lesen.
2. Neuen Plan `posts/plan/<JJJJ>-W<KW>.json` schreiben: 14 Posts mit date, time, audience, format, layout, palette, file, headline, body, footer, cta, caption. Dateiname: `posts/<JJJJ-MM>/<datum>-<HHMM>-<zielgruppe>-<stichwort>.png`.
3. `python3 tools/render.py posts/plan/<woche>.json` (vorher ggf. `pip install playwright --break-system-packages && python3 -m playwright install chromium`).
4. Jedes Bild ansehen (z. B. Übersichtsbild) und auf abgeschnittenen Text prüfen.
5. Commit + Push nach `main`.
6. Jeden Post in Metricool einplanen: Facebook + Instagram, `draft: false`, `autoPublish: true`, Bild-URL `https://raw.githubusercontent.com/gr-werkbank-salzburg/ralnova-social/main/<file>`, mediaAltText = Überschrift.
7. Mit `getScheduledPosts` prüfen, dass alle 14 Posts drin sind.

## Stories (1 pro Tag, 14:00, Instagram + Facebook)
Das Team postet zusätzlich selbst echte Stories aus dem Arbeitsalltag. Unsere automatische Story ergänzt das, sie ersetzt es nicht.

- Format: animiertes Video 1080×1920, 10 Sekunden, mit eigener Musik. Vorlagen: `tools/stories/intro.html` (Aussage/Vorstellung) und `tools/stories/frage.html` (Frage mit A/B/C). Für jede Story eine neue HTML-Datei `tools/stories/<datum>-<stichwort>.html` anlegen, aufgebaut wie die Vorlagen (Flex-Spalte, `padding:290px 96px 340px`, damit oben und unten die Instagram-Bedienelemente nichts verdecken; Elemente erscheinen nacheinander per CSS-Animation, letztes Element spätestens nach ~6,5 s).
- Abwechseln über die Woche: Farbwelten aus der Palette oben, Hintergrundbewegung (Streifen, Glow, Kreise, Linien …) und Story-Typ:
  - Frage mit A/B/C, Antwort per Nachricht (Umfrage-Sticker gehen automatisch nicht)
  - Ein Satz / eine These, groß, Zeile für Zeile
  - Kurzer Tipp in 3 Schritten
  - „Neuer Beitrag im Feed“: Überschrift des heutigen Feed-Posts anteasern
  - Wer wir sind / was wir machen
  - Mythos vs. Wahrheit
- Abwechselnd Betriebe (Sie/ihr) und Handwerker (du) ansprechen. Gleiche harte Regeln wie bei den Posts.
- Musik: `python3 tools/make_music.py tools/music/<datum>.wav 10 <variant>` (variant = Wochentag 0–6, damit jede Story etwas anders klingt). Nur selbst erzeugte Musik verwenden, nie fremde Songs.
- Rendern: `python3 tools/render_story.py tools/stories/<datei>.html posts/stories/<datum>-<stichwort>.mp4 10 tools/music/<datum>.wav`. Danach Standbilder bei Sekunde 1,5 / 3,5 / 5,5 / 9,5 prüfen (nichts überlappt, nichts abgeschnitten).
- Einplanen: providers instagram + facebook, `instagramData {"type":"STORY"}`, `facebookData {"type":"STORY"}`, KEIN `text`, media = Raw-URL der MP4.
