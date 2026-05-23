import React, { useState } from 'react';
import './FAQ.css';

function FAQ() {
  const [activeIndex, setActiveIndex] = useState(null);

  const faqs = [
    {
      question: "How accurate is the AI skin analysis?",
      answer: "Our AI model has been trained on thousands of dermatological images and achieves approximately 95% accuracy in identifying common skin conditions. However, it's important to note that this tool is designed to provide preliminary insights and should not replace professional medical diagnosis. For any concerning skin conditions, we always recommend consulting with a qualified dermatologist."
    },
    {
      question: "What types of skin conditions can be detected?",
      answer: "SkinAnalyzer can identify 23 different skin conditions including acne, eczema, psoriasis, rosacea, melanoma, atopic dermatitis, ringworm, warts, herpes, shingles, chicken pox, measles, cellulitis, urticaria (hives), and various other common dermatological conditions. Our AI analyzes skin texture, color, patterns, and other visual characteristics to provide accurate assessments."
    },
    {
      question: "Is my personal data and photos secure?",
      answer: "Yes, absolutely. We take your privacy very seriously. All uploaded images are processed securely and are stored encrypted in our database. Your personal information is protected according to industry-standard security protocols. We never share your data with third parties, and you have full control over your information. You can delete your account and all associated data at any time."
    },
    {
      question: "How should I take photos for the best results?",
      answer: "For optimal results, follow these guidelines: 1) Use good natural lighting or bright indoor lighting. 2) Keep your camera steady and in focus. 3) Capture the affected area clearly, filling most of the frame. 4) Avoid shadows, glare, or reflections. 5) Include some surrounding healthy skin for context. 6) Take photos from a distance of 6-12 inches. 7) Ensure the image is not blurry or pixelated. Multiple angles can also help provide a more comprehensive analysis."
    },
    {
      question: "How much does SkinAnalyzer cost?",
      answer: "SkinAnalyzer is currently free to use! We believe everyone should have access to preliminary skin health insights. Simply create a free account and you can start analyzing your skin conditions immediately. There are no hidden fees or subscription charges. Our mission is to democratize access to dermatological insights and empower individuals to take control of their skin health."
    },
    {
      question: "Can I use SkinAnalyzer if I have sensitive skin?",
      answer: "Yes, SkinAnalyzer is a non-invasive, photo-based analysis tool that works for all skin types, including sensitive skin. Since the analysis is done through photographs, there's no physical contact or products applied to your skin. However, if you have sensitive skin and receive recommendations for treatments or products, always patch test new products and consult with a dermatologist before trying new skincare routines."
    },
    {
      question: "How long does the analysis take?",
      answer: "The AI analysis is very fast! Once you upload your photo, the analysis typically takes only 3-5 seconds to complete. You'll receive instant results showing the top 3 most likely skin conditions with confidence percentages, detailed descriptions, and a downloadable PDF report. The entire process from upload to receiving your comprehensive report takes less than a minute."
    },
    {
      question: "What if I'm not satisfied with my results?",
      answer: "If you're not satisfied with your results, we recommend: 1) Retaking the photo with better lighting and focus. 2) Trying different angles of the affected area. 3) Ensuring the skin condition is clearly visible in the image. Remember, SkinAnalyzer provides preliminary insights and should not replace professional medical advice. If you have concerns about your skin condition, we strongly encourage you to consult with a board-certified dermatologist who can provide a proper diagnosis and treatment plan."
    }
  ];

  const toggleFAQ = (index) => {
    setActiveIndex(activeIndex === index ? null : index);
  };

  return (
    <div className="faq-page">
      <div className="faq-container">
        <div className="faq-header">
          <h1>Common Questions</h1>
          <p>Click on any question to see the answer</p>
        </div>

        <div className="faq-list">
          {faqs.map((faq, index) => (
            <div key={index} className="faq-item">
              <button
                className={`faq-question ${activeIndex === index ? 'active' : ''}`}
                onClick={() => toggleFAQ(index)}
              >
                <span>{faq.question}</span>
                <span className="faq-icon">▼</span>
              </button>
              <div className={`faq-answer ${activeIndex === index ? 'active' : ''}`}>
                <div className="faq-answer-content">
                  {faq.answer}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default FAQ;
