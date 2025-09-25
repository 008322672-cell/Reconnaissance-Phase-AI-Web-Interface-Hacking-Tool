import requests
import gradio as gr

SAFE_HEADERS = [
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Strict-Transport-Security",  # Only relevant over HTTPS
]

def check_headers(url: str) -> dict:
    """
    Educational tool: checks common security headers on a URL you own or have permission to assess.
    Returns a JSON-like dict with header presence and a simple score.
    """
    url = (url or "").strip()
    if not url.startswith(("http://", "https://")):
        return {"error": "Please include http:// or https:// in the URL."}

    try:
        resp = requests.get(url, timeout=10)
    except Exception as e:
        return {"error": f"Request failed: {e}"}

    headers = {k.title(): v for k, v in resp.headers.items()}  # Canonicalize
    results = {}
    for h in SAFE_HEADERS:
        if h == "Strict-Transport-Security" and not resp.url.startswith("https://"):
            results[h] = "N/A (only applicable to HTTPS)"
        else:
            results[h] = headers.get(h, "MISSING")

    # Compute a simple score (count headers that are present and applicable)
    applicable = [h for h in SAFE_HEADERS if not (h == "Strict-Transport-Security" and not resp.url.startswith("https://"))]
    present_count = sum(1 for h in applicable if results[h] != "MISSING")

    summary = {
        "final_url": resp.url,
        "status_code": resp.status_code,
        "present_headers": present_count,
        "applicable_headers": len(applicable),
        "score": f"{present_count}/{len(applicable)}"
    }
    summary.update(results)
    return summary

with gr.Blocks() as demo:
    gr.Markdown(
        "# Web Security Header Checker (Educational)\n"
        "Only assess systems you own or have explicit permission to test."
    )
    url = gr.Textbox(label="URL (include http/https)", placeholder="https://example.com")
    btn = gr.Button("Check")
    out = gr.JSON(label="Results")
    btn.click(fn=check_headers, inputs=url, outputs=out)

if __name__ == "__main__":
    # share=True is encouraged so you can submit the public link from Gradio
    demo.launch(share=True)
