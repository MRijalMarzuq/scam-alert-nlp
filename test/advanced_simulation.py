"""
SCAM ALERT - Advanced Simulation & Visualization
Simulasi real-time dengan visualisasi interaktif dan analisis mendalam
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from main import ScamDetector
import time
from datetime import datetime, timedelta
import random

class AdvancedSimulator:
    def __init__(self):
        self.detector = ScamDetector()
        self.history = []
        
    def load_model(self):
        """Load trained model"""
        try:
            self.detector.load_model('scam_detector_model.pkl')
            return True
        except FileNotFoundError:
            print("❌ Model not found! Run main.py first.")
            return False
    
    def simulate_message_stream(self, duration_seconds=30):
        """Simulate real-time message stream"""
        print("\n" + "="*70)
        print("📡 REAL-TIME MESSAGE STREAM SIMULATION")
        print("="*70)
        print(f"Duration: {duration_seconds} seconds")
        print("Monitoring incoming messages...\n")
        
        # Sample messages pool
        messages_pool = {
            'scam': [
                "SELAMAT! Anda menang 100 juta! Transfer admin 500rb",
                "URGENT! Bank account will be blocked. Click here now!",
                "Investasi 1 juta jadi 10 juta! Guaranteed profit!",
                "FREE iPhone 15! Pay shipping $50 only!",
                "Pinjaman cepat cair! Bunga 0%! Tanpa survei!",
            ],
            'legitimate': [
                "Meeting reminder: Tomorrow at 2 PM",
                "Your package has been delivered successfully",
                "Invoice #12345 sent. Please review and confirm",
                "Thank you for your order. Tracking: JNE123456",
                "Project deadline extended to next week",
            ]
        }
        
        start_time = time.time()
        message_count = 0
        scam_blocked = 0
        
        while (time.time() - start_time) < duration_seconds:
            # Random message selection
            msg_type = random.choice(['scam', 'legitimate'])
            if random.random() < 0.3:  # 30% scam rate
                msg_type = 'scam'
            
            message = random.choice(messages_pool[msg_type])
            
            # Detect
            result = self.detector.predict(message)
            message_count += 1
            
            # Display
            timestamp = datetime.now().strftime("%H:%M:%S")
            if result['is_scam']:
                scam_blocked += 1
                print(f"[{timestamp}] ⚠️  BLOCKED: {message[:45]}... ({result['confidence']:.1f}%)")
            else:
                print(f"[{timestamp}] ✅ ALLOWED: {message[:45]}... ({result['confidence']:.1f}%)")
            
            # Record history
            self.history.append({
                'timestamp': timestamp,
                'message': message,
                'prediction': result['prediction'],
                'confidence': result['confidence'],
                'actual_type': msg_type
            })
            
            # Random delay
            time.sleep(random.uniform(0.5, 2.0))
        
        # Summary
        print(f"\n{'='*70}")
        print("📊 STREAM SUMMARY")
        print('='*70)
        print(f"Total Messages:  {message_count}")
        print(f"Scam Blocked:    {scam_blocked}")
        print(f"Safe Allowed:    {message_count - scam_blocked}")
        print(f"Block Rate:      {(scam_blocked/message_count)*100:.1f}%")
        
        return pd.DataFrame(self.history)
    
    def analyze_detection_patterns(self):
        """Analyze detection patterns dari history"""
        if not self.history:
            print("⚠️  No history data. Run simulation first.")
            return
        
        df = pd.DataFrame(self.history)
        
        print("\n" + "="*70)
        print("🔍 DETECTION PATTERN ANALYSIS")
        print("="*70)
        
        # Accuracy calculation
        df['correct'] = df['prediction'] == df['actual_type']
        accuracy = df['correct'].mean() * 100
        
        print(f"\n📊 Performance Metrics:")
        print(f"   Accuracy:        {accuracy:.2f}%")
        print(f"   Total Analyzed:  {len(df)}")
        print(f"   Correct:         {df['correct'].sum()}")
        print(f"   Incorrect:       {(~df['correct']).sum()}")
        
        # Confusion matrix
        print(f"\n📈 Detection Breakdown:")
        print(pd.crosstab(df['actual_type'], df['prediction'], 
                          rownames=['Actual'], colnames=['Predicted']))
        
        # Confidence analysis
        print(f"\n🎯 Confidence Statistics:")
        print(f"   Mean:   {df['confidence'].mean():.2f}%")
        print(f"   Median: {df['confidence'].median():.2f}%")
        print(f"   Min:    {df['confidence'].min():.2f}%")
        print(f"   Max:    {df['confidence'].max():.2f}%")
        
        # Visualize
        self.visualize_patterns(df)
    
    def visualize_patterns(self, df):
        """Create comprehensive visualizations"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Prediction distribution
        ax1 = fig.add_subplot(gs[0, 0])
        pred_counts = df['prediction'].value_counts()
        colors = ['#ff6b6b' if x == 'scam' else '#51cf66' for x in pred_counts.index]
        ax1.bar(pred_counts.index, pred_counts.values, color=colors)
        ax1.set_title('Messages by Prediction', fontweight='bold')
        ax1.set_ylabel('Count')
        for i, v in enumerate(pred_counts.values):
            ax1.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')
        
        # 2. Confidence distribution
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.hist(df['confidence'], bins=20, color='#4c6ef5', edgecolor='black', alpha=0.7)
        ax2.axvline(df['confidence'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["confidence"].mean():.1f}%')
        ax2.set_title('Confidence Score Distribution', fontweight='bold')
        ax2.set_xlabel('Confidence (%)')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        
        # 3. Accuracy over time
        ax3 = fig.add_subplot(gs[1, :])
        df['cumulative_accuracy'] = df['correct'].expanding().mean() * 100
        ax3.plot(df.index, df['cumulative_accuracy'], linewidth=2, color='#4c6ef5')
        ax3.fill_between(df.index, df['cumulative_accuracy'], alpha=0.3)
        ax3.set_title('Cumulative Accuracy Over Time', fontweight='bold')
        ax3.set_xlabel('Message Number')
        ax3.set_ylabel('Accuracy (%)')
        ax3.grid(alpha=0.3)
        ax3.axhline(y=90, color='green', linestyle='--', label='90% Target')
        ax3.legend()
        
        # 4. Confusion Matrix Heatmap
        ax4 = fig.add_subplot(gs[2, 0])
        cm = pd.crosstab(df['actual_type'], df['prediction'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd', ax=ax4,
                   xticklabels=['Legitimate', 'Scam'],
                   yticklabels=['Legitimate', 'Scam'])
        ax4.set_title('Confusion Matrix', fontweight='bold')
        ax4.set_ylabel('Actual')
        ax4.set_xlabel('Predicted')
        
        # 5. Confidence by prediction type
        ax5 = fig.add_subplot(gs[2, 1])
        df.boxplot(column='confidence', by='prediction', ax=ax5)
        ax5.set_title('Confidence by Prediction Type', fontweight='bold')
        ax5.set_xlabel('Prediction')
        ax5.set_ylabel('Confidence (%)')
        plt.suptitle('')  # Remove default title
        
        plt.suptitle('SCAM ALERT - Detection Pattern Analysis', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        plt.savefig('simulation_analysis.png', dpi=300, bbox_inches='tight')
        print("\n📊 Visualization saved: simulation_analysis.png")
        plt.show()
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        print("\n" + "="*70)
        print("🔬 EDGE CASE TESTING")
        print("="*70)
        
        edge_cases = {
            "Ambiguous - Mixed Signals": [
                "Hai, mau investasi? Modal kecil untung besar. Tapi legit kok, bukan scam",
                "Meeting urgent besok! Jangan lupa transfer biaya parkir 50rb dulu ya",
            ],
            "Very Short Messages": [
                "Menang!",
                "Urgent!",
                "Thanks",
                "OK",
            ],
            "Very Long Messages": [
                "Selamat pagi, saya ingin menginformasikan bahwa paket Anda telah sampai di kantor pos cabang terdekat. Mohon untuk segera mengambil paket tersebut dengan membawa KTP asli dan nomor resi pengiriman. Kantor pos buka dari jam 8 pagi hingga 4 sore setiap hari kerja. Terima kasih atas perhatiannya."
            ],
            "Multiple Languages": [
                "Hello! Anda menang lottery! Please transfer fee $100 untuk claim prize!",
                "Selamat! You won the jackpot! Hubungi 08123456789 now!",
            ],
            "Numbers and URLs": [
                "Transfer ke 1234567890 nominal Rp 5.000.000 untuk aktivasi",
                "Klik http://bit.ly/12345 untuk verifikasi akun Anda",
                "Download app di https://play.google.com/store/apps",
            ],
            "ALL CAPS vs lowercase": [
                "URGENT URGENT URGENT TRANSFER NOW!!!",
                "urgent please transfer money now",
            ],
            "Legitimate but Urgent": [
                "URGENT: Meeting moved to 10 AM. Please confirm ASAP!",
                "IMPORTANT: Project deadline today! Submit now!",
            ]
        }
        
        results = []
        
        for category, messages in edge_cases.items():
            print(f"\n{'='*70}")
            print(f"📂 {category}")
            print('='*70)
            
            for msg in messages:
                result = self.detector.predict(msg)
                status = "⚠️ SCAM" if result['is_scam'] else "✅ SAFE"
                
                print(f"\nMessage: {msg}")
                print(f"Result:  {status} (Confidence: {result['confidence']:.2f}%)")
                
                results.append({
                    'category': category,
                    'message': msg,
                    'prediction': status,
                    'confidence': result['confidence']
                })
        
        return pd.DataFrame(results)
    
    def stress_test(self, num_messages=100):
        """Performance stress testing"""
        print("\n" + "="*70)
        print(f"⚡ PERFORMANCE STRESS TEST ({num_messages} messages)")
        print("="*70)
        
        # Generate random messages
        test_messages = [
            f"Test message {i}: This is a sample text for stress testing the system"
            for i in range(num_messages)
        ]
        
        # Time the predictions
        print(f"\n🔄 Processing {num_messages} messages...")
        start_time = time.time()
        
        results = []
        for i, msg in enumerate(test_messages):
            if (i + 1) % 20 == 0:
                print(f"   Processed: {i+1}/{num_messages}")
            
            result = self.detector.predict(msg)
            results.append(result)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Results
        print(f"\n📊 Performance Results:")
        print(f"   Total Messages:     {num_messages}")
        print(f"   Total Time:         {duration:.2f} seconds")
        print(f"   Average Time:       {(duration/num_messages)*1000:.2f} ms/message")
        print(f"   Throughput:         {num_messages/duration:.2f} messages/second")
        
        # Memory usage estimation
        import sys
        model_size = sys.getsizeof(self.detector) / (1024 * 1024)
        print(f"   Est. Memory Usage:  {model_size:.2f} MB")
        
        return results
    
    def comparative_model_analysis(self, test_messages):
        """Compare all models side by side"""
        print("\n" + "="*70)
        print("🔄 COMPARATIVE MODEL ANALYSIS")
        print("="*70)
        
        model_results = {name: [] for name in self.detector.models.keys()}
        
        print(f"\nTesting {len(test_messages)} messages across all models...\n")
        
        for msg in test_messages:
            print(f"Message: {msg[:50]}...")
            print("-" * 70)
            
            for model_name in self.detector.models.keys():
                result = self.detector.predict(msg, model_name=model_name)
                status = "⚠️ SCAM" if result['is_scam'] else "✅ SAFE"
                print(f"   {model_name:<25} → {status} ({result['confidence']:.1f}%)")
                
                model_results[model_name].append({
                    'message': msg,
                    'prediction': result['prediction'],
                    'confidence': result['confidence']
                })
            print()
        
        # Agreement analysis
        print("\n📊 Model Agreement Analysis:")
        
        # Calculate agreement rate
        predictions = []
        for model_name in self.detector.models.keys():
            preds = [r['prediction'] for r in model_results[model_name]]
            predictions.append(preds)
        
        agreement_count = sum(1 for i in range(len(test_messages)) 
                             if len(set(pred[i] for pred in predictions)) == 1)
        
        print(f"   Perfect Agreement: {agreement_count}/{len(test_messages)} "
              f"({(agreement_count/len(test_messages))*100:.1f}%)")
        
        # Average confidence by model
        print(f"\n🎯 Average Confidence by Model:")
        for model_name in self.detector.models.keys():
            avg_conf = np.mean([r['confidence'] for r in model_results[model_name]])
            print(f"   {model_name:<25} → {avg_conf:.2f}%")


def main():
    """Main simulation interface"""
    print("\n" + "="*70)
    print("🛡️  SCAM ALERT - ADVANCED SIMULATION & ANALYSIS")
    print("="*70)
    
    simulator = AdvancedSimulator()
    
    if not simulator.load_model():
        return
    
    print("\n✅ Model loaded successfully!")
    
    while True:
        print("\n" + "="*70)
        print("📋 SIMULATION MENU")
        print("="*70)
        print("1. Real-Time Message Stream (30s)")
        print("2. Analyze Detection Patterns")
        print("3. Test Edge Cases")
        print("4. Performance Stress Test")
        print("5. Comparative Model Analysis")
        print("6. Full Simulation Suite")
        print("0. Exit")
        
        choice = input("\n🎯 Select option (0-6): ").strip()
        
        if choice == '1':
            df = simulator.simulate_message_stream(duration_seconds=30)
            save = input("\n💾 Save stream data? (y/n): ").strip().lower()
            if save == 'y':
                df.to_csv('message_stream.csv', index=False)
                print("✅ Saved to message_stream.csv")
        
        elif choice == '2':
            simulator.analyze_detection_patterns()
        
        elif choice == '3':
            df = simulator.test_edge_cases()
            save = input("\n💾 Save edge case results? (y/n): ").strip().lower()
            if save == 'y':
                df.to_csv('edge_cases.csv', index=False)
                print("✅ Saved to edge_cases.csv")
        
        elif choice == '4':
            num = input("Enter number of messages (default 100): ").strip()
            num = int(num) if num.isdigit() else 100
            simulator.stress_test(num)
        
        elif choice == '5':
            print("\n📝 Enter test messages (empty line to finish):")
            messages = []
            while True:
                msg = input(f"{len(messages)+1}. ").strip()
                if not msg:
                    break
                messages.append(msg)
            
            if messages:
                simulator.comparative_model_analysis(messages)
        
        elif choice == '6':
            print("\n🚀 Running Full Simulation Suite...")
            print("This will take approximately 2-3 minutes...\n")
            
            input("Press Enter to start...")
            
            # Run all simulations
            print("\n[1/4] Message Stream Simulation...")
            simulator.simulate_message_stream(20)
            
            print("\n[2/4] Pattern Analysis...")
            simulator.analyze_detection_patterns()
            
            print("\n[3/4] Edge Case Testing...")
            simulator.test_edge_cases()
            
            print("\n[4/4] Stress Test...")
            simulator.stress_test(50)
            
            print("\n✅ Full simulation suite completed!")
        
        elif choice == '0':
            print("\n👋 Exiting simulation...")
            break
        
        else:
            print("❌ Invalid option!")


if __name__ == "__main__":
    main()