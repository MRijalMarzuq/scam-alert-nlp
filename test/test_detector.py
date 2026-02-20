"""
SCAM ALERT - Interactive Testing & Simulation
Testing real-time dengan berbagai skenario
"""

from main import ScamDetector
import pandas as pd
import time
import os

class ScamDetectorTester:
    def __init__(self):
        self.detector = None
        self.test_results = []
    
    def load_model(self):
        """Load trained model"""
        try:
            self.detector = ScamDetector()
            self.detector.load_model('scam_detector_model.pkl')
            return True
        except FileNotFoundError:
            print("\n❌ ERROR: Model belum di-training!")
            print("💡 Jalankan 'python main.py' terlebih dahulu")
            return False
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "="*70)
        print(f"   {title}")
        print("="*70)
    
    def analyze_message(self, message, show_detail=True):
        """Analyze single message dengan detail"""
        result = self.detector.predict(message)
        
        if show_detail:
            print(f"\n📩 Message:")
            print(f"   {message}")
            print(f"\n🔍 Analysis:")
            print(f"   Status:     {'⚠️  SCAM DETECTED' if result['is_scam'] else '✅ SAFE/LEGITIMATE'}")
            print(f"   Confidence: {result['confidence']:.2f}%")
            print(f"   Model Used: {result['model_used']}")
            
            if result['is_scam']:
                print(f"\n🚨 WARNING:")
                print(f"   • DO NOT click any suspicious links")
                print(f"   • DO NOT provide personal information (KTP, password, PIN)")
                print(f"   • DO NOT transfer money to unknown accounts")
                print(f"   • Verify directly with official sources if unsure")
            else:
                print(f"\nℹ️  This message appears legitimate.")
                print(f"   However, always verify sensitive requests.")
        
        return result
    
    def compare_models(self, message):
        """Compare results from all models"""
        print(f"\n📩 Message: {message}")
        print(f"\n🔍 Comparing Results from All Models:")
        print("-"*70)
        
        results = []
        for model_name in self.detector.models.keys():
            result = self.detector.predict(message, model_name=model_name)
            status = "⚠️  SCAM" if result['is_scam'] else "✅ SAFE"
            confidence = result['confidence']
            
            print(f"   {model_name:<25} → {status:<10} (Confidence: {confidence:>6.2f}%)")
            results.append({
                'model': model_name,
                'prediction': status,
                'confidence': confidence
            })
        
        return results
    
    def batch_test(self, messages, show_individual=False):
        """Test multiple messages"""
        self.print_header("🧪 BATCH TESTING")
        
        results = []
        for i, msg in enumerate(messages, 1):
            if show_individual:
                print(f"\n{'='*70}")
                print(f"Test Case {i}/{len(messages)}")
            
            result = self.analyze_message(msg, show_detail=show_individual)
            results.append({
                'message': msg[:50] + '...' if len(msg) > 50 else msg,
                'prediction': '⚠️ SCAM' if result['is_scam'] else '✅ SAFE',
                'confidence': f"{result['confidence']:.2f}%"
            })
            
            if not show_individual:
                status = '⚠️ SCAM' if result['is_scam'] else '✅ SAFE'
                print(f"{i}. {status:<10} ({result['confidence']:.1f}%) - {msg[:40]}...")
        
        # Summary
        df = pd.DataFrame(results)
        scam_count = len([r for r in results if '⚠️' in r['prediction']])
        safe_count = len(results) - scam_count
        
        print(f"\n📊 Summary:")
        print(f"   Total Tested: {len(results)}")
        print(f"   Scam Detected: {scam_count}")
        print(f"   Safe Messages: {safe_count}")
        
        return df
    
    def interactive_mode(self):
        """Interactive testing mode"""
        self.print_header("🎮 INTERACTIVE MODE")
        print("Type your message to analyze (or 'exit' to quit)")
        print("Commands: 'compare' - compare all models | 'help' - show help")
        
        while True:
            print("\n" + "-"*70)
            user_input = input("📝 Enter message: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Exiting interactive mode...")
                break
            
            if not user_input:
                print("⚠️  Please enter a message!")
                continue
            
            if user_input.lower() == 'help':
                print("\n💡 Available Commands:")
                print("   • Type any message to analyze")
                print("   • 'compare' - Compare results from all models")
                print("   • 'exit/quit/q' - Exit interactive mode")
                continue
            
            if user_input.lower() == 'compare':
                msg = input("📝 Enter message to compare: ").strip()
                if msg:
                    self.compare_models(msg)
                continue
            
            # Analyze message
            self.analyze_message(user_input)
            
            # Ask for model comparison
            choice = input("\n❓ Compare with all models? (y/n): ").strip().lower()
            if choice == 'y':
                self.compare_models(user_input)
    
    def run_test_suite(self):
        """Run comprehensive test suite"""
        self.print_header("🧪 COMPREHENSIVE TEST SUITE")
        
        test_suites = {
            "Undian Palsu / Fake Lottery": [
                "SELAMAT! Anda menang undian Rp 100 juta! Transfer admin 500rb ke 08123456789",
                "Congratulations! You won $1,000,000! Send processing fee $100 now!",
                "ANDA PEMENANG! Hadiah 50 juta menanti! Hubungi 08123456789 segera!",
            ],
            "Phishing Banking": [
                "URGENT! Akun BCA Anda akan diblokir. Verifikasi di http://fake-bca.com sekarang",
                "Your account has been compromised. Reset password: http://fake-bank.com",
                "Mandiri Alert: Transaksi mencurigakan. Konfirmasi segera atau diblokir!",
            ],
            "Investasi Bodong / Investment Scam": [
                "Investasi modal 1 juta jadi 10 juta dalam sebulan! DIJAMIN! WA 08123456789",
                "CRYPTOCURRENCY! 1000% return guaranteed! Limited slots available!",
                "Trading forex profit 200% per hari! Modal 500rb jadi 10jt! Terbukti!",
            ],
            "Pinjaman Online Ilegal": [
                "Pinjaman 20 juta cair hari ini! Tanpa jaminan! KTP saja! Call 08111222333",
                "DANA DARURAT! Bunga 0%! Approved dalam 1 jam! Transfer admin 300rb",
            ],
            "Legitimate - Business Communication": [
                "Meeting besok jam 2 siang. Jangan lupa bawa laptop dan dokumen proposal",
                "Invoice bulan ini sudah saya kirim via email. Mohon dicek dan konfirmasi",
                "Report sudah selesai. Saya upload di Google Drive. Link sudah dikirim",
            ],
            "Legitimate - Personal Communication": [
                "Hai, kapan bisa ketemu? Mau diskusi project bareng kamu minggu depan",
                "Terima kasih sudah datang ke acara kemarin. Senang bisa bertemu!",
                "Selamat ulang tahun! Semoga panjang umur dan sehat selalu",
            ],
            "Legitimate - Notifications": [
                "Paket Anda sudah sampai di kantor pos. Silakan ambil dengan bawa KTP",
                "Reminder: Deadline tugas besar tanggal 15 Desember. Jangan telat ya!",
                "Jadwal training minggu depan Senin-Rabu. Lokasi di kantor pusat",
            ]
        }
        
        all_results = []
        
        for category, messages in test_suites.items():
            print(f"\n{'='*70}")
            print(f"📂 Category: {category}")
            print('='*70)
            
            for i, msg in enumerate(messages, 1):
                result = self.detector.predict(msg)
                status = "⚠️  SCAM" if result['is_scam'] else "✅ SAFE"
                
                print(f"\n{i}. {msg}")
                print(f"   → {status} (Confidence: {result['confidence']:.2f}%)")
                
                all_results.append({
                    'category': category,
                    'message': msg[:50] + '...' if len(msg) > 50 else msg,
                    'prediction': status,
                    'confidence': result['confidence']
                })
        
        # Overall summary
        df = pd.DataFrame(all_results)
        print(f"\n{'='*70}")
        print("📊 OVERALL SUMMARY")
        print('='*70)
        print(f"\nTotal Messages Tested: {len(all_results)}")
        print(f"\nBy Prediction:")
        print(df['prediction'].value_counts().to_string())
        print(f"\nAverage Confidence: {df['confidence'].mean():.2f}%")
        
        return df
    
    def simulate_real_scenario(self):
        """Simulate real-world scenario"""
        self.print_header("🎬 REAL-WORLD SCENARIO SIMULATION")
        
        scenarios = [
            {
                'title': "Scenario 1: Suspicious Lottery Win",
                'messages': [
                    "SELAMAT! Anda menang undian BCA senilai Rp 50.000.000",
                    "Untuk klaim hadiah, transfer biaya admin Rp 500.000 ke rekening 1234567890",
                    "Hubungi customer service kami di 08123456789 untuk proses lebih lanjut"
                ]
            },
            {
                'title': "Scenario 2: Normal Business Communication",
                'messages': [
                    "Halo, saya dari PT ABC ingin konfirmasi jadwal meeting besok",
                    "Agenda: Presentasi proposal kerjasama, jam 14.00 WIB",
                    "Mohon konfirmasi kehadiran Anda. Terima kasih"
                ]
            },
            {
                'title': "Scenario 3: Phishing Attempt",
                'messages': [
                    "URGENT! Akun Anda terdeteksi login dari lokasi tidak dikenal",
                    "Segera verifikasi akun Anda di link berikut: http://fake-verification.com",
                    "Jika tidak diverifikasi dalam 24 jam, akun akan diblokir permanen"
                ]
            }
        ]
        
        for scenario in scenarios:
            print(f"\n{'='*70}")
            print(f"📱 {scenario['title']}")
            print('='*70)
            
            scam_detected = False
            for i, msg in enumerate(scenario['messages'], 1):
                print(f"\nMessage {i}: {msg}")
                result = self.detector.predict(msg, show_detail=False)
                
                time.sleep(0.5)  # Simulate processing
                
                if result['is_scam']:
                    print(f"   → ⚠️  SCAM DETECTED! (Confidence: {result['confidence']:.2f}%)")
                    scam_detected = True
                else:
                    print(f"   → ✅ Safe (Confidence: {result['confidence']:.2f}%)")
            
            print(f"\n🎯 Scenario Assessment:")
            if scam_detected:
                print("   ⚠️  THIS IS A SCAM ATTEMPT!")
                print("   🚨 ACTION: Block sender and report to authorities")
            else:
                print("   ✅ This appears to be legitimate communication")
                print("   ℹ️  ACTION: Proceed with normal caution")
    
    def show_statistics(self):
        """Show model statistics"""
        self.print_header("📊 MODEL STATISTICS")
        
        print("\n🤖 Available Models:")
        for name, data in self.detector.models.items():
            marker = "⭐" if name == self.detector.best_model_name else "  "
            print(f"   {marker} {name}")
        
        print(f"\n🏆 Best Model: {self.detector.best_model_name}")
        print(f"\n💡 TF-IDF Features: {len(self.detector.vectorizer.get_feature_names_out())}")
        
        # Top features
        print(f"\n🔝 Top 15 Important Keywords:")
        feature_names = self.detector.vectorizer.get_feature_names_out()
        
        # Get feature importance from Random Forest if available
        if 'Random Forest' in self.detector.models:
            rf_model = self.detector.models['Random Forest']['model']
            importances = rf_model.feature_importances_
            indices = importances.argsort()[-15:][::-1]
            
            for i, idx in enumerate(indices, 1):
                print(f"   {i:2d}. {feature_names[idx]:<20} (importance: {importances[idx]:.4f})")


def main():
    """Main testing interface"""
    print("\n" + "="*70)
    print("🛡️  SCAM ALERT - TESTING & SIMULATION INTERFACE")
    print("="*70)
    
    tester = ScamDetectorTester()
    
    # Load model
    if not tester.load_model():
        return
    
    print("\n✅ Model loaded successfully!")
    
    # Main menu
    while True:
        print("\n" + "="*70)
        print("📋 TESTING MENU")
        print("="*70)
        print("1. Interactive Mode (Manual Input)")
        print("2. Run Test Suite (Comprehensive Testing)")
        print("3. Batch Test (Multiple Messages)")
        print("4. Real-World Scenario Simulation")
        print("5. Model Statistics")
        print("6. Compare Models")
        print("0. Exit")
        
        choice = input("\n🎯 Select option (0-6): ").strip()
        
        if choice == '1':
            tester.interactive_mode()
        
        elif choice == '2':
            results_df = tester.run_test_suite()
            
            save = input("\n💾 Save results to CSV? (y/n): ").strip().lower()
            if save == 'y':
                filename = 'test_suite_results.csv'
                results_df.to_csv(filename, index=False)
                print(f"✅ Results saved to {filename}")
        
        elif choice == '3':
            print("\n📝 Enter messages (one per line, empty line to finish):")
            messages = []
            while True:
                msg = input(f"{len(messages)+1}. ").strip()
                if not msg:
                    break
                messages.append(msg)
            
            if messages:
                show_detail = input("\nShow detailed analysis? (y/n): ").strip().lower() == 'y'
                results_df = tester.batch_test(messages, show_individual=show_detail)
        
        elif choice == '4':
            tester.simulate_real_scenario()
        
        elif choice == '5':
            tester.show_statistics()
        
        elif choice == '6':
            msg = input("\n📝 Enter message to compare: ").strip()
            if msg:
                tester.compare_models(msg)
        
        elif choice == '0':
            print("\n👋 Thank you for using SCAM ALERT!")
            print("🛡️  Stay safe from scams!")
            break
        
        else:
            print("❌ Invalid option! Please select 0-6")


if __name__ == "__main__":
    main()