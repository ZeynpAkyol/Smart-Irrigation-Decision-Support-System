import pandas as pd
import numpy as np

def veri_seti_uret(satir_sayisi=2000): 
    np.random.seed(42)
    
    bitkiler = [
        "Domates", "Biber", "Çilek", "Lavanta", "Kaktüs", 
        "Mısır", "Ayçiçeği", "Gül", "Orkide", "Zeytin Ağacı"
    ]
    
    su_katsayilari = {
        0: 15, 1: 12, 2: 10, 3: 5, 4: 2, 
        5: 18, 6: 14, 7: 13, 8: 7, 9: 4
    }
    
    bitki_kodlari = np.random.randint(0, len(bitkiler), satir_sayisi)
    
    data = {
        'sicaklik': np.random.uniform(10, 45, satir_sayisi), 
        'nem': np.random.uniform(5, 95, satir_sayisi),      
        'isik': np.random.randint(0, 3, satir_sayisi), 
        'bitki_turu_kod': bitki_kodlari
    }
    
    df = pd.DataFrame(data)
    

    df['katsayi'] = df['bitki_turu_kod'].map(su_katsayilari)
    
    
    df['su_miktari'] = (df['sicaklik'] * 1.5) - (df['nem'] * 0.5) + (df['isik'] * 10) + df['katsayi'] + 20
    

    df['su_miktari'] = df['su_miktari'].clip(lower=0)
    
    noise = np.random.normal(0, 2, satir_sayisi)
    df['su_miktari'] = df['su_miktari'] + noise
    
    df = df.drop(columns=['katsayi'])
    
    df.to_csv("bitki_verisi.csv", index=False)
    print(f"✅ {len(bitkiler)} farklı bitki türü içeren {satir_sayisi} satırlık veri seti 'bitki_verisi.csv' olarak hazır!")

if __name__ == "__main__":
    veri_seti_uret()