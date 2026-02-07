import pandas as pd

def split_csv(file_path, lines_per_file):
    # قراءة الملف CSV بشكل جزئي
    chunk_iter = pd.read_csv(file_path, chunksize=lines_per_file)

    for i, chunk in enumerate(chunk_iter):
        # حفظ الجزء الجديد إلى ملف CSV
        chunk.to_csv(f'part_{i + 1}.csv', index=False)

# استخدم المسار الكامل للملف هنا
split_csv(r'D:\ABOOD PORT\jan31_PH_oh_rmmm\jan31_PH_oh_rmmm.csv', 5500000)
