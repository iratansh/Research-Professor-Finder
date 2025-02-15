# textVector.py
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

app = FastAPI(title="Professor Matchmaker", version="1.0")

# Mock database data
professors = [
    {
        "name": "Dr. Alice Chen",
        "department": "Computer Science",
        "research_description": "Research Personal website Multimedia Research Group: http://crome.cs.ualberta.ca/mrc/ Areas Remote Sensing Data Science Human Perception in Data Science Multimedia Graphics & Visualization Computer Vision, Pattern Recognition and Multimedia Communications Interests My research interests include multimedia data transmission and Quality of Experience (QoE), mesh simplification and Levels-of-Detail, 3DTV, 3D textured mesh visualization, image processing and adaptive learning/assessment. I introduced the concept of Just-Noticeable-Difference (JND) and Relative Change on 3D TexMesh in the scale-space domain - validated following psychophysical two-alternative-choice methodology. Summary My research focus is on the analysis of multimedia patterns and their human perceptual impacts on real-world applications, e.g., animation, education, surveillance and healthcare. My techniques are built upon mathematical formulations like Random-Walks, Set Partitioning in Hierarchical Tree (SPIHT), Conditional Random Field (CRF), Scale-Space Filtering and Just-Noticeable-Difference (JND). Projects include: Improved automatic multi-exposure image fusion and correspondence; introduced perceptually enhanced techniques for automatic segmentation using visual cues and for enhancing medical or photographic image quality; motion capture data compression and transmission; multi-object tracking. The Computer Reinforced Online Multimedia Education (CROME) framework, which focused on adaptive learning/assessment, was designed and prototyped during the period from 2006-2012. More recent research is focused on Intelligent Analysis of Signal Decomposition and Aggregation in different application domains, which include satellite signal (InSAR) filtering and coherence estimation, LiDAR point cloud modelling, Parkinson's Disease progress tracking, vital sign pattern recognition and pressure injury monitoring.",
    },
    {
        "name": "Dr. Raj Patel",
        "biology": "Biology",
        "research_description": "Research Dr. Maria Cutumisu is an Associate Professor in the Department of Educational and Counselling Psychology, Faculty of Education, McGill University in the area of Learning Sciences. Previously, she was a tenured Associate Professor in the Department of Educational Psychology, Faculty of Education, at the University of Alberta in the area of Measurement, Evaluation, and Data Science and an Adjunct Professor in the Department of Computing Science at the University of Alberta. She graduated with an M.Sc. and a Ph.D. in Computing Science from the Department of Computing Science, University of Alberta and she trained as a postdoctoral scholar in Learning Sciences in the AAA Lab at the Stanford Graduate School of Education. Her research in the Assessment of Learning and Transfer (ALERT) lab draws on computing science and education and has been funded by tri-council grants and scholarships as a PI (NSERC DG, NSERC CGS-D, SSHRC IG, and SSHRC IDG) and as a co-PI (SSHRC IG, and SSHRC IDG, and CIHR). Her research interests include feedback processing (SSHRC IDG grant), machine learning and educational data mining techniques for automated feedback generation (NSERC DG), game-based assessments that support learning and performance-based learning (SSHRC IG grants), computational thinking (e.g., CanCode Callysto grants, CCTt tests, and SSHRC IG), AI in games (e.g., reinforcement learning in computer role-playing games), serious games (e.g., the RETAIN game for neonatal resuscitation), and virtual character (i.e., agent) behaviours in interactive computer games with applications in education. She has employed learning analytics to investigate the impact of K-16 students’ choices (e.g., willingness to choose critical feedback from interactive virtual characters and to revise digital posters) on learning outcomes and mindset within an online game-based assessment environment to understand how prepared students are to learn and innovate. She uses psychophysiological techniques (e.g., eye-tracking and electrodermal activity wearables) to provide a comprehensive understanding of students' learning and memory processes (SSHRC, Killam). She is also affiliated with the Centre for Research in Applied Measurement and Evaluation (CRAME), Centre for the Studies of Asphyxia and Resuscitation (CSAR), EdTeKLA, AI4Society, Centre for Mathematics, Science, and Technology Education (CMASTE), Neuroscience and Mental Health Institute (NMHI) at the University of Alberta, and Women and Children’s Health Research Institute (WCHRI).",
    },
    {
        "name": "Dr. Maria Lopez",
        "department": "Engineering",
        "research_description": "With the aim of advancing personalized treatment options for complex medical disorders, my professional goal centers around the application of data science and artificial intelligence. My educational background encompasses a master's degree in medical biotechnology specializing in human genetics, a master's degree in computer science, and a Ph.D. in neuropsychiatry focusing on brain imaging in mental disorders. Additionally, I have undergone extensive post-doctoral training at the Alberta Machine Intelligence Institute (AMII), recognized as one of Canada's leading centers of excellence in artificial intelligence. This diverse foundation provides me with a unique perspective and expertise in tackling medical problems through data analytical techniques, while also fostering effective collaboration with experts across disciplines. Over the past decade, I have had the privilege of co-supervising graduate students and international interns in both computing science and biomedical domains. This experience has allowed me to nurture the growth of aspiring researchers while contributing to the development of cutting-edge projects. During this time, my team and I have successfully developed, evaluated, and deployed machine learning models using a wide range of structured and unstructured real-world healthcare datasets. By combining my expertise in medical biotechnology, neuroscience, data science, and artificial intelligence, along with my fervor for interdisciplinary collaboration and mentoring, I am well-equipped to address biomedical challenges with innovative and data-driven approaches.",
    },
]

# Load ML model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(query: str) -> List[dict]:
    # Encode query and descriptions
    query_embedding = model.encode([query])
    descriptions = [p["research_description"] for p in professors]
    doc_embeddings = model.encode(descriptions)

    # Calculate similarities
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    # Add scores to results
    results = []
    for i, prof in enumerate(professors):
        results.append({**prof, "similarity_score": float(similarities[i])})

    return sorted(results, key=lambda x: x["similarity_score"], reverse=True)


@app.get("/search")
async def search_professors(query: str):
    """Search endpoint for professor matching"""
    return calculate_similarity(query)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
