**Summary**
Research Professor Finder web application that helps students find and connect with professors at the University of Alberta based on research interests. Here's a breakdown of the key components and technologies:

**Frontend (React.js):**
- Built with React and React Router for navigation
- Features a modern UI with animated backgrounds and floating icons
- Includes search functionality, professor listings, and detailed professor profiles
- Uses Tailwind CSS for styling
- Has email tips generation for contacting professors
- Implements smooth transitions and loading states

**Backend (Python/FastAPI):**
- FastAPI server handling API endpoints for:
  - Professor matching
  - Email tips generation
  - Professor information retrieval
- Features a sophisticated text preprocessing and matching system using:
  - NLTK for text processing
  - Sentence Transformers for semantic matching
  - Cosine similarity for relevance scoring
  - Custom QuickSort implementation for result ranking

**Data Collection:**
- Includes a web scraper built with Playwright
- Asynchronously scrapes professor information from the university directory
- Stores data in SQLite database with professor details including:
  - Contact information
  - Faculty affiliations
  - Research overviews
  - Course information

**Integration with AI:**
- Uses the DeepSeek LLM through OpenRouter API for generating email tips
- Implements semantic search using the all-MiniLM-L6-v2 model

**The architecture follows a modern client-server pattern with:**
- Clear separation of concerns
- RESTful API endpoints
- Efficient data processing
- Responsive UI design
- Error handling and loading states
- Cross-Origin Resource Sharing (CORS) support

Credits: Ishaan Ratanshi, Taha Kamil, Sayuj Tiwari, Sammipyia Poharel, Ali Zaedi