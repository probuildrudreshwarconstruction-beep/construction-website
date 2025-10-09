/* ===== Global Styles ===== */
body, .stApp {
    margin:0;
    padding:0;
    font-family:"Open Sans", sans-serif;
    background:#000;
    color:#f2f2f2;
}

/* ===== Hero Section ===== */
.hero {
    position: relative;
    width: 100%;
    height: 90vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 5px solid red; /* Red frame */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

.hero-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: #fff;
    background: rgba(0,0,0,0.3);
    padding: 20px 40px;
    border-radius: 8px;
    z-index: 2;
}
.hero-content h1 {
    font-size: 3rem;
    color: #ffcc00;
}
.hero-content p {
    font-size: 1.3rem;
}

/* ===== Project Showcase Cards ===== */
.project-showcase-card {
    display: flex;
    flex-wrap: wrap;
    background: #111;
    border-radius: 10px;
    margin-bottom: 30px;
    overflow: hidden;
    box-shadow: 0 0 15px rgba(255,204,0,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.project-showcase-card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(255,204,0,0.5);
}
.project-showcase-card .project-media {
    flex: 1;
    min-width: 300px;
    cursor: pointer;
    overflow: hidden;
}
.project-showcase-card .project-media img,
.project-showcase-card .project-media video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
    transition: transform 0.3s ease;
}
.project-showcase-card .project-media:hover img,
.project-showcase-card .project-media:hover video {
    transform: scale(1.05);
}
.project-showcase-card .project-info {
    flex: 1;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.project-showcase-card .project-info h3 {
    font-size: 1.8rem;
    color: #ffcc00;
    margin-bottom: 10px;
}
.project-showcase-card .project-info p {
    font-size: 1rem;
    margin-bottom: 8px;
    line-height: 1.5;
}
.project-showcase-card .project-info button {
    width: fit-content;
    margin-top: 10px;
    background: #ffcc00;
    color: #000;
    border: none;
    border-radius: 5px;
    padding: 8px 16px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.3s ease;
}
.project-showcase-card .project-info button:hover {
    background: #e6b800;
}

/* ===== Modal Styles ===== */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    padding-top: 60px;
    left: 0; top: 0;
    width: 100%; height: 100%;
    overflow: auto;
    background: rgba(0,0,0,0.95);
}
.modal-close {
    position: absolute;
    top: 20px;
    right: 35px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
}
#mediaModal h2 {
    color: #ffcc00;
    margin-bottom: 10px;
}
#mediaModal p {
    color: #fff;
    margin-bottom: 5px;
}
#mediaModal img, #mediaModal video {
    width: 100%;
    max-height: 70vh;
    border-radius: 8px;
    margin-bottom: 15px;
}

/* ===== Who We Are, What We Do, Contact CTA ===== */
.who-we-are, .what-we-do, .contact-cta {
    padding: 50px 20px;
    text-align: center;
}
.who-we-are h2, .what-we-do h2, .contact-cta h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #ffcc00;
}
.who-we-are p, .what-we-do p, .contact-cta p {
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 15px;
}
.contact-cta .cta-buttons {
    margin-top: 20px;
}
.contact-cta .cta-button {
    background: #ffcc00;
    color: #000;
    border: none;
    border-radius: 5px;
    padding: 12px 20px;
    margin: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s ease;
}
.contact-cta .cta-button:hover {
    background: #e6b800;
}

/* ===== Footer ===== */
footer {
    background: #000;
    color: #fff;
    text-align: center;
    padding: 20px;
}
footer a {
    color: #ffcc00;
    text-decoration: none;
}
footer a:hover {
    text-decoration: underline;
}

/* ===== Responsive ===== */
@media(max-width:768px){
    .hero-content h1{ font-size:2rem; }
    .hero-content p{ font-size:1rem; }
    .project-showcase-card{ flex-direction: column; }
    .project-showcase-card .project-media { min-height: 200px; }
    .contact-cta .cta-button{ width: 80%; margin: 5px auto; display: block; }
}
@media(max-width:480px){
    .hero-content h1{ font-size:1.5rem; }
    .project-showcase-card .project-media { min-height: 150px; }
    .contact-cta .cta-button{ padding: 8px 16px; font-size:0.9rem; }
}

