from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

job_data = pd.read_csv('jobs.csv')

questions = [
    "Apa bidang pekerjaan yang Anda minati?",
    "Apa keahlian yang Anda kuasai?(Hard Skill)",
    "Apa bidang pendidikan terakhir yang Anda tempuh?(cth: informatika)",
    "Apakah Anda memiliki pengalaman kerja sebelumnya? (Ya/Tidak)",
    "Apakah Anda memiliki sertifikasi atau pelatihan terkait? (Ya/Tidak)",
    "Berapa tingkat kesediaan Anda untuk berpergian atau bekerja di luar kota? (1-5)",
    "Berapa lama Anda bersedia untuk bekerja dalam sehari? (jam)",
    "Apakah Anda lebih suka bekerja secara tim atau mandiri?",
    "Apakah Anda memiliki keterampilan komunikasi yang baik? (Ya/Tidak)",
    "Bagaimana tingkat kemampuan bahasa Inggris Anda? (1-5)"
]

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    answers = [request.form.get(f'q{i}') for i in range(len(questions))]

    job_data['Score'] = 0
    job_data['Reasons'] = ''
    for i, row in job_data.iterrows():
        reasons = []
        if answers[0].lower() in row['title'].lower():
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda tertarik pada bidang ini.")
        if set(answers[1].lower().split()) & set(row['skills'].lower().split(';')):
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda memiliki keterampilan yang dibutuhkan.")
        if answers[2].lower() in row['education'].lower():
            job_data.at[i, 'Score'] += 1
            reasons.append("Pendidikan Anda sesuai.")
        if answers[3].lower() == row['experience'].lower():
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda memiliki pengalaman yang relevan.")
        if answers[4].lower() == row['certification'].lower():
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda memiliki sertifikasi yang relevan.")
        if int(answers[5]) >= int(row['travel']):
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda bersedia untuk berpergian.")
        if int(answers[6]) >= int(row['hours']):
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda bersedia untuk bekerja sesuai jam yang dibutuhkan.")
        if answers[7].lower() == row['team'].lower():
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda lebih suka bekerja dalam tim.")
        if answers[8].lower() == row['communication'].lower():
            job_data.at[i, 'Score'] += 1
            reasons.append("Anda memiliki keterampilan komunikasi yang baik.")
        if int(answers[9]) >= int(row['english']):
            job_data.at[i, 'Score'] += 1
            reasons.append("Kemampuan bahasa Inggris Anda memadai.")
        
        job_data.at[i, 'Reasons'] = "; ".join(reasons)

    recommended_jobs = job_data.sort_values(by='Score', ascending=False)
    top_jobs = recommended_jobs.head(2)
    all_jobs = recommended_jobs[['title', 'Score']]

    result_text = ""
    for i, job in top_jobs.iterrows():
        result_text += f"Watashi pikir pekerjaan paling cocok untuk Anda adalah {job['title']} karena {job['description']}. Alasan: {job['Reasons']}. "

    return render_template('result.html', result_text=result_text, recommended_jobs=recommended_jobs, top_jobs=top_jobs, all_jobs=all_jobs)

if __name__ == '__main__':
    app.run(debug=True)
