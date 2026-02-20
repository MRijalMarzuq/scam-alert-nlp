from main import ScamDetector

detector = ScamDetector()
detector.load_model('scam_detector_model.pkl')

test_messages = [
    "URGENT! Transfer 500rb untuk klaim hadiah 10 juta!",
    "Reminder: Meeting besok jam 10 pagi",
    "Investasi modal 1 juta jadi 100 juta dijamin!",
    "Invoice bulan ini sudah dikirim via email",
]

print("\n" + "="*70)
print("QUICK BATCH TEST")
print("="*70)

for i, msg in enumerate(test_messages, 1):
    result = detector.predict(msg)
    status = "⚠️ SCAM" if result['is_scam'] else "✅ SAFE"
    print(f"\n{i}. {msg}")
    print(f"   → {status} (Confidence: {result['confidence']:.1f}%)")