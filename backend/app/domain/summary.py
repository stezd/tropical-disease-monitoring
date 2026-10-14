"""Plain-text summary for the copy button and the QR page. No name, NIK, or photo."""

from app.domain.warnings import missing_vitals
from app.triage.content import NONE_ID, FlowContent, Option, RouteId
from app.triage.schemas import Answers, RankedDisease
from app.triage.scoring import bmi, companion_shown


def _fmt(n: float) -> str:
    return f"{n:g}"


def summary(
    answers: Answers,
    content: FlowContent,
    route: RouteId,
    top: RankedDisease | None,
    unknown: bool,
) -> str:
    """Plain-text summary for the copy button and the QR page. No name, NIK, or photo."""
    flow = content.flow
    a = answers

    def label(options: list[Option], oid: str | None) -> str | None:
        return next((o.text for o in options if o.id == oid), None)

    cluster = next((c for c in flow.clusters if c.id == a.complaint), None)
    if cluster:
        complaint = cluster.name
    elif a.complaint == NONE_ID:
        complaint = "tidak ada keluhan (cek risiko)"
    else:
        complaint = "-"
    pattern_q = flow.patterns.get(a.complaint or "")
    pattern = label(pattern_q.options, a.pattern) if pattern_q else None
    companion_q = flow.companions.get(a.complaint or "")
    companions = (
        [o.text for o in companion_q.options if o.id in a.companion and o.id != NONE_ID]
        if companion_q and companion_shown(companion_q, a)
        else []
    )
    eco = [o.reason or o.text for o in flow.eco if o.id in a.eco and o.id != NONE_ID]
    flags = [f for f in flow.red_flags if f.id in a.red_flags]
    b = bmi(a)
    no_thermo, no_bp = missing_vitals(a, content)
    proxies = [
        o.text
        for opts in flow.vital_proxies.values()
        for o in opts
        if o.id in a.vital_proxy and o.id != NONE_ID
    ]
    if b is not None and a.height_cm is not None and a.weight_kg is not None:
        gizi = f"IMT {b:.1f} (TB {_fmt(a.height_cm)} cm, BB {_fmt(a.weight_kg)} kg)"
    else:
        gizi = "proksi: " + (label(flow.nutrition_proxies, a.nutrition_proxy) or "-")
    body = [r.name for r in flow.body_regions if r.id in a.body]
    pain = f" (nyeri {a.pain}/10)" if body and a.pain is not None else ""
    findings = [o.text for o in flow.findings if o.id in a.findings and o.id != NONE_ID]
    disease = content.diseases[top.id] if top else None
    r = flow.routes[route]
    when = a.taken_at.strftime("%d/%m/%Y %H.%M") if a.taken_at else "-"

    if unknown:
        dugaan = "belum dapat ditentukan"
    elif top and disease:
        dugaan = f"{disease.name} ({top.pct}%)"
    else:
        dugaan = "-"

    patient = [
        label(flow.who, a.who) or "-",
        f"{a.age} th" if a.age is not None else "-",
        label(flow.sex, a.sex) or "-",
    ]
    if a.pregnant is not None:
        patient.append("hamil" if a.pregnant else "tidak hamil")

    lines = [
        "TROPICARE – RANGKUMAN SKRINING",
        f"Tanggal   : {when}",
        "Pasien    : " + " · ".join(patient),
        "Tanda bahaya: " + ("; ".join(f.text for f in flags) if flags else "tidak ada"),
        f"Keluhan   : {complaint}",
        f"Pola      : {pattern or '-'}",
        f"Penyerta  : {'; '.join(companions) if companions else '-'}",
        f"{flow.eco_label:<10}: {'; '.join(eco) if eco else 'tidak ada'}",
        f"Obat      : {a.drugs.strip() or '-'}",
    ]
    if "temp" in flow.vitals:
        if no_thermo:
            temp = "tidak diukur (tidak punya termometer)"
        elif a.temp is not None:
            temp = f"{a.temp:.1f} °C"
        else:
            temp = "-"
        lines.append(f"Suhu      : {temp}")
    if "bp" in flow.vitals:
        if no_bp:
            bp = "tidak diukur (tidak punya tensimeter)"
        elif a.bp_sys is not None and a.bp_dia is not None:
            bp = f"{a.bp_sys}/{a.bp_dia} mmHg"
        else:
            bp = "-"
        lines.append(f"Tensi     : {bp}")
    if "glucose" in flow.vitals:
        lines.append(
            f"Gula darah: {_fmt(a.glucose) + ' mg/dL' if a.glucose is not None else '-'}"
        )
    if no_thermo or no_bp:
        lines.append(f"Proksi    : {'; '.join(proxies) if proxies else 'tidak ada'}")
    lines.append(f"Gizi      : {gizi}")
    if flow.measure_waist:
        lines.append(
            f"Lingkar perut: {_fmt(a.waist_cm) + ' cm' if a.waist_cm is not None else '-'}"
        )
    if flow.body_regions:
        lines.append(f"Peta nyeri: {', '.join(body) + pain if body else '-'}")
    lines += [
        f"Foto      : {', '.join(findings) if findings else '-'}",
        f"Lab       : {'; '.join(disease.lab) if disease and disease.lab else '-'}",
        f"Dugaan    : {dugaan}",
        f"Rute      : {r.name} – {r.sub}",
    ]
    return "\n".join(lines)
