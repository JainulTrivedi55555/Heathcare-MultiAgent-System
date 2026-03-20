from coordinator import HealthcareCoordinator


def main():
    print("\n" + "═" * 60)
    print("   HEALTHCARE MULTI-AGENT SYSTEM — CLI")
    print("═" * 60)
    print("⚠️  For informational purposes only. Not a substitute for medical advice.\n")

    patient_name = input("Enter patient name: ").strip()
    if not patient_name:
        patient_name = "Anonymous"

    print("\nDescribe the patient's symptoms (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    symptoms = " ".join(lines).strip()

    if not symptoms:
        print("No symptoms provided. Exiting.")
        return

    coordinator = HealthcareCoordinator()
    results = coordinator.handle_patient(patient_name, symptoms)
    coordinator.print_results(results)


if __name__ == "__main__":
    main()
