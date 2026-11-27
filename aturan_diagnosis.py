
import pandas as pd


FILE_GEJALA = "dataset/Daftar_Gejala_Tomat_9_Kategori_ID.csv"


def load_knowledge_base():
    data = pd.read_csv(FILE_GEJALA, encoding="utf-8-sig")

    knowledge_base = {}

    for disease in data["Disease"].unique():
        symptoms = data.loc[
            data["Disease"] == disease,
            "Kode_Gejala"
        ].tolist()

        knowledge_base[disease] = symptoms

    return knowledge_base


def build_rules(knowledge_base):
    """
    Membentuk aturan IF-THEN dari basis pengetahuan.
    IF kode gejala ditemukan
    THEN kategori penyakit menjadi kandidat diagnosis.
    """

    rules = []

    for disease, symptoms in knowledge_base.items():
        for symptom in symptoms:
            rules.append({
                "fakta": symptom,
                "kesimpulan": disease
            })

    return rules


def forward_chaining(selected_symptoms, knowledge_base):
    """
    Menjalankan Forward Chaining berdasarkan fakta gejala
    yang dipilih pengguna.
    """

    rules = build_rules(knowledge_base)

    facts = set(selected_symptoms)
    results = {}

    # Proses pencocokan fakta dengan aturan
    for rule in rules:

        if rule["fakta"] in facts:
            disease = rule["kesimpulan"]

            if disease not in results:
                results[disease] = []

            results[disease].append(rule["fakta"])

    # Menyusun hasil diagnosis
    diagnosis_results = []

    for disease, matched_symptoms in results.items():

        total_symptoms = len(knowledge_base[disease])
        total_match = len(matched_symptoms)

        percentage = (
            total_match / total_symptoms
        ) * 100

        diagnosis_results.append({
            "penyakit": disease,
            "jumlah_cocok": total_match,
            "total_gejala": total_symptoms,
            "persentase": round(percentage, 2),
            "gejala_cocok": matched_symptoms
        })

    # Urutkan berdasarkan jumlah dan persentase kecocokan
    diagnosis_results.sort(
        key=lambda item: (
            item["jumlah_cocok"],
            item["persentase"]
        ),
        reverse=True
    )

    return diagnosis_results


if __name__ == "__main__":

    knowledge_base = load_knowledge_base()
    rules = build_rules(knowledge_base)

    print("BASIS PENGETAHUAN SISTEM PAKAR")

    for disease, symptoms in knowledge_base.items():
        print(f"- {disease}: {len(symptoms)} gejala")

    print(f"\nTotal kategori: {len(knowledge_base)}")
    print(f"Total aturan IF-THEN: {len(rules)}")

    print("\nCONTOH ATURAN:")
    for rule in rules[:5]:
        print(
            f"IF {rule['fakta']} "
            f"THEN {rule['kesimpulan']}"
        )

    print("\nPENGUJIAN FORWARD CHAINING")

    for disease, symptoms in knowledge_base.items():

        selected_symptoms = symptoms[:3]

        results = forward_chaining(
            selected_symptoms,
            knowledge_base
        )

        print(f"\nPengujian: {disease}")
        print(f"Gejala dipilih: {len(selected_symptoms)}")

        for result in results:
            print(f"Kategori: {result['penyakit']}")
            print(
                f"Kecocokan: {result['jumlah_cocok']}/"
                f"{result['total_gejala']}"
            )
            print(
                f"Persentase: {result['persentase']}%"
            )
