from html import escape

def _svg(body: str, height: int = 220) -> str:
    return f"""
    <div style="width:100%;overflow-x:auto;margin:12px 0;">
        <svg viewBox="0 0 720 {height}"
             width="100%"
             style="max-width:720px;height:auto;display:block;margin:auto;"
             xmlns="http://www.w3.org/2000/svg">
            {body}
        </svg>
    </div>
    """


def confusion_matrix(tp, fn, fp, tn, positive="Positive", negative="Negative"):
    return _svg(f"""
        <text x="360" y="25" text-anchor="middle"
              font-size="17" font-weight="700">Confusion Matrix</text>

        <text x="470" y="55" text-anchor="middle"
              font-size="13">Predicted</text>

        <text x="360" y="82" text-anchor="middle"
              font-size="13">Actual</text>

        <text x="430" y="105" text-anchor="middle"
              font-size="13">{escape(positive)}</text>
        <text x="570" y="105" text-anchor="middle"
              font-size="13">{escape(negative)}</text>

        <text x="320" y="140" text-anchor="middle"
              font-size="13">{escape(positive)}</text>
        <text x="320" y="190" text-anchor="middle"
              font-size="13">{escape(negative)}</text>

        <rect x="365" y="115" width="130" height="55"
              fill="#e8f5e9" stroke="#777"/>
        <rect x="495" y="115" width="130" height="55"
              fill="#ffebee" stroke="#777"/>
        <rect x="365" y="170" width="130" height="55"
              fill="#ffebee" stroke="#777"/>
        <rect x="495" y="170" width="130" height="55"
              fill="#e8f5e9" stroke="#777"/>

        <text x="430" y="150" text-anchor="middle"
              font-size="18" font-weight="700">TP = {tp}</text>
        <text x="560" y="150" text-anchor="middle"
              font-size="18" font-weight="700">FN = {fn}</text>
        <text x="430" y="205" text-anchor="middle"
              font-size="18" font-weight="700">FP = {fp}</text>
        <text x="560" y="205" text-anchor="middle"
              font-size="18" font-weight="700">TN = {tn}</text>
    """, 245)


def probability_threshold(probability, threshold):
    return _svg(f"""
        <text x="360" y="25" text-anchor="middle"
              font-size="17" font-weight="700">
            Predicted Probability
        </text>

        <line x1="80" y1="170" x2="650" y2="170"
              stroke="#555" stroke-width="2"/>

        <path d="M80 165
                 C170 160 190 80 280 75
                 C370 70 390 155 470 165
                 C540 172 600 170 650 170"
              fill="none" stroke="#555" stroke-width="3"/>

        <line x1="{80 + probability * 570}" y1="55"
              x2="{80 + probability * 570}" y2="175"
              stroke="#777" stroke-width="2"
              stroke-dasharray="6,5"/>

        <line x1="{80 + threshold * 570}" y1="45"
              x2="{80 + threshold * 570}" y2="175"
              stroke="#222" stroke-width="3"
              stroke-dasharray="8,5"/>

        <text x="{80 + probability * 570}" y="42"
              text-anchor="middle" font-size="13">
            Probability = {probability:.2f}
        </text>

        <text x="{80 + threshold * 570}" y="195"
              text-anchor="middle" font-size="13">
            Threshold = {threshold:.2f}
        </text>

        <text x="80" y="195" text-anchor="middle" font-size="12">0.0</text>
        <text x="365" y="195" text-anchor="middle" font-size="12">0.5</text>
        <text x="650" y="195" text-anchor="middle" font-size="12">1.0</text>
    """, 220)



def precision_visual(predicted_defaults=120, actual_defaults=90):
    """Visualize only the quantities explicitly given in C17."""
    precision = actual_defaults / predicted_defaults * 100
    other_predictions = predicted_defaults - actual_defaults

    return _svg(f"""
        <text x="360" y="25" text-anchor="middle"
              font-size="17" font-weight="700">
            Precision — Predicted Defaults
        </text>

        <text x="360" y="52" text-anchor="middle"
              font-size="13">
            Predicted defaults = {predicted_defaults}
        </text>

        <rect x="140" y="78" width="440" height="62"
              fill="#f5f5f5" stroke="#777"/>

        <rect x="140" y="78" width="330" height="62"
              fill="#e8f5e9" stroke="#777"/>

        <rect x="470" y="78" width="110" height="62"
              fill="#ffebee" stroke="#777"/>

        <text x="305" y="106" text-anchor="middle"
              font-size="14" font-weight="700">
            Actually defaulted
        </text>

        <text x="305" y="130" text-anchor="middle"
              font-size="18" font-weight="700">
            {actual_defaults}
        </text>

        <text x="525" y="106" text-anchor="middle"
              font-size="13">
            Other predicted
        </text>

        <text x="525" y="130" text-anchor="middle"
              font-size="16" font-weight="700">
            {other_predictions}
        </text>

        <text x="360" y="175" text-anchor="middle"
              font-size="14">
            Precision = actual positives ÷ predicted positives
        </text>

        <text x="360" y="205" text-anchor="middle"
              font-size="17" font-weight="700">
            {actual_defaults} ÷ {predicted_defaults} = {precision:.0f}%
        </text>
    """, 225)

def roc_curve(auc_a=0.79, auc_b=0.86):
    return _svg(f"""
        <text x="360" y="24" text-anchor="middle"
              font-size="17" font-weight="700">ROC Curve</text>

        <line x1="80" y1="180" x2="650" y2="180"
              stroke="#555" stroke-width="2"/>
        <line x1="80" y1="180" x2="80" y2="45"
              stroke="#555" stroke-width="2"/>

        <line x1="80" y1="180" x2="650" y2="45"
              stroke="#aaa" stroke-dasharray="7,6"/>

        <path d="M80 180
                 C130 115 175 95 240 78
                 C330 58 410 52 650 45"
              fill="none" stroke="#555" stroke-width="4"/>

        <path d="M80 180
                 C120 95 170 70 250 58
                 C350 45 470 43 650 45"
              fill="none" stroke="#222" stroke-width="4"/>

        <text x="500" y="95" font-size="13">
            Model A: AUC = {auc_a:.2f}
        </text>
        <text x="500" y="115" font-size="13">
            Model B: AUC = {auc_b:.2f}
        </text>

        <text x="365" y="215" text-anchor="middle"
              font-size="13">False Positive Rate</text>

        <text x="20" y="115" text-anchor="middle"
              font-size="13"
              transform="rotate(-90 20 115)">
            True Positive Rate
        </text>
    """, 235)


def elbow_plot():
    points = [
        (100, 50), (190, 88), (280, 118),
        (370, 138), (460, 150), (550, 158)
    ]

    path = " ".join(
        ("M" if i == 0 else "L") + f"{x} {y}"
        for i, (x, y) in enumerate(points)
    )

    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="6" fill="#555"/>'
        for x, y in points
    )

    labels = "".join(
        f'<text x="{x}" y="185" text-anchor="middle" font-size="12">{i}</text>'
        for i, (x, y) in enumerate(points, start=1)
    )

    return _svg(f"""
        <text x="360" y="24" text-anchor="middle"
              font-size="17" font-weight="700">
            Elbow Method
        </text>

        <line x1="80" y1="165" x2="620" y2="165"
              stroke="#555" stroke-width="2"/>
        <line x1="80" y1="165" x2="80" y2="45"
              stroke="#555" stroke-width="2"/>

        <path d="{path}" fill="none"
              stroke="#555" stroke-width="4"/>

        {circles}
        {labels}

        <text x="350" y="215" text-anchor="middle"
              font-size="13">Number of Clusters (K)</text>

        <text x="22" y="110" text-anchor="middle"
              font-size="13"
              transform="rotate(-90 22 110)">
            Within-Cluster Sum of Squares
        </text>
    """, 235)


def kmeans_diagram():
    return _svg("""
        <text x="360" y="28" text-anchor="middle"
              font-size="18" font-weight="700">
            K-means Clustering
        </text>

        <!-- Cluster 1 -->
        <circle cx="185" cy="100" r="8" fill="#555"/>
        <circle cx="225" cy="118" r="8" fill="#555"/>
        <circle cx="160" cy="132" r="8" fill="#555"/>
        <circle cx="205" cy="150" r="8" fill="#555"/>
        <circle cx="245" cy="142" r="8" fill="#555"/>
        <circle cx="175" cy="165" r="8" fill="#555"/>

        <!-- Cluster 1 centroid -->
        <circle cx="198" cy="135" r="19"
                fill="white"
                stroke="#222"
                stroke-width="3"/>
        <text x="198" y="141" text-anchor="middle"
              font-size="15" font-weight="700">
            C1
        </text>

        <!-- Cluster 2 -->
        <circle cx="475" cy="105" r="8" fill="#777"/>
        <circle cx="520" cy="120" r="8" fill="#777"/>
        <circle cx="455" cy="135" r="8" fill="#777"/>
        <circle cx="500" cy="150" r="8" fill="#777"/>
        <circle cx="540" cy="145" r="8" fill="#777"/>
        <circle cx="480" cy="170" r="8" fill="#777"/>

        <!-- Cluster 2 centroid -->
        <circle cx="495" cy="137" r="19"
                fill="white"
                stroke="#222"
                stroke-width="3"/>
        <text x="495" y="143" text-anchor="middle"
              font-size="15" font-weight="700">
            C2
        </text>

        <!-- Assignment examples -->
        <line x1="160" y1="132" x2="198" y2="135"
              stroke="#999" stroke-width="1.5"
              stroke-dasharray="5,4"/>
        <line x1="225" y1="118" x2="198" y2="135"
              stroke="#999" stroke-width="1.5"
              stroke-dasharray="5,4"/>
        <line x1="455" y1="135" x2="495" y2="137"
              stroke="#999" stroke-width="1.5"
              stroke-dasharray="5,4"/>
        <line x1="520" y1="120" x2="495" y2="137"
              stroke="#999" stroke-width="1.5"
              stroke-dasharray="5,4"/>

        <!-- Labels -->
        <text x="198" y="205" text-anchor="middle"
              font-size="14" font-weight="600">
            Cluster 1
        </text>

        <text x="495" y="205" text-anchor="middle"
              font-size="14" font-weight="600">
            Cluster 2
        </text>

        <text x="360" y="238" text-anchor="middle"
              font-size="14">
            Assign observations to the nearest cluster center
        </text>
    """, 255)


def actual_predicted():
    return _svg("""
        <text x="360" y="24" text-anchor="middle"
              font-size="17" font-weight="700">
            Actual vs Predicted
        </text>

        <line x1="80" y1="180" x2="650" y2="180"
              stroke="#555" stroke-width="2"/>
        <line x1="80" y1="180" x2="80" y2="45"
              stroke="#555" stroke-width="2"/>

        <line x1="80" y1="180" x2="650" y2="45"
              stroke="#aaa" stroke-width="2"
              stroke-dasharray="7,6"/>

        <circle cx="160" cy="155" r="6" fill="#555"/>
        <circle cx="220" cy="140" r="6" fill="#555"/>
        <circle cx="285" cy="125" r="6" fill="#555"/>
        <circle cx="350" cy="115" r="6" fill="#555"/>
        <circle cx="420" cy="90" r="6" fill="#555"/>
        <circle cx="500" cy="75" r="6" fill="#555"/>

        <text x="365" y="215" text-anchor="middle"
              font-size="13">Predicted</text>
        <text x="25" y="115" text-anchor="middle"
              font-size="13"
              transform="rotate(-90 25 115)">
            Actual
        </text>
    """, 235)


def residual_plot():
    return _svg("""
        <text x="360" y="24" text-anchor="middle"
              font-size="17" font-weight="700">
            Residual Plot
        </text>

        <line x1="80" y1="125" x2="650" y2="125"
              stroke="#777" stroke-width="2"
              stroke-dasharray="6,5"/>

        <line x1="80" y1="180" x2="650" y2="180"
              stroke="#555" stroke-width="2"/>
        <line x1="80" y1="180" x2="80" y2="45"
              stroke="#555" stroke-width="2"/>

        <circle cx="130" cy="118" r="5" fill="#555"/>
        <circle cx="190" cy="132" r="5" fill="#555"/>
        <circle cx="250" cy="120" r="5" fill="#555"/>
        <circle cx="310" cy="138" r="5" fill="#555"/>
        <circle cx="370" cy="108" r="5" fill="#555"/>
        <circle cx="430" cy="145" r="5" fill="#555"/>
        <circle cx="490" cy="92" r="5" fill="#555"/>
        <circle cx="550" cy="155" r="5" fill="#555"/>
        <circle cx="610" cy="72" r="5" fill="#555"/>

        <text x="365" y="215" text-anchor="middle"
              font-size="13">Fitted Values</text>
        <text x="25" y="115" text-anchor="middle"
              font-size="13"
              transform="rotate(-90 25 115)">
            Residuals
        </text>
    """, 235)


def render_visual(q):
    """
    Return a lightweight inline visual for a quiz question.

    Returns an empty string when the question does not have
    a supported visual or when the visual would require
    inventing information not present in the question.
    """

    qid = q.get("Question_ID")

    # Existing bank visuals
    if qid == "C04":
        return probability_threshold(0.73, 0.50)

    if qid == "C17":
        return precision_visual(120, 90)

    if qid == "C20":
        return confusion_matrix(84, 16, 24, 176,
                                positive="Positive",
                                negative="Negative")

    if qid == "C22":
        return roc_curve(0.79, 0.86)

    if qid == "R06":
        return actual_predicted()

    if qid == "R20":
        return residual_plot()

    if qid == "CL15":
        return kmeans_diagram()

    if qid == "CL16":
        return elbow_plot()

    return ""