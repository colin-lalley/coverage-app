import React, { useState } from 'react';
import { Building2, Users, Laptop, Shield, AlertCircle } from 'lucide-react';

const InsuranceAssessment = () => {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({
    industry: '',
    employees: '',
    revenue: '',
    hasPhysicalLocation: null,
    handlesCustomerData: null,
    hasBoard: null,
    providesAdvice: null,
    hasVehicles: null
  });
  const [showResults, setShowResults] = useState(false);

  const questions = [
    {
      id: 'industry',
      question: 'What industry is your company in?',
      type: 'select',
      options: [
        'Technology/SaaS',
        'Professional Services',
        'E-commerce/Retail',
        'Healthcare',
        'Financial Services',
        'Manufacturing',
        'Construction',
        'Food & Beverage',
        'Other'
      ]
    },
    {
      id: 'employees',
      question: 'How many employees do you have?',
      type: 'select',
      options: ['1-10', '11-50', '51-200', '201-500', '500+']
    },
    {
      id: 'revenue',
      question: 'What is your annual revenue?',
      type: 'select',
      options: ['Under $1M', '$1M-$5M', '$5M-$10M', '$10M-$50M', 'Over $50M']
    },
    {
      id: 'hasPhysicalLocation',
      question: 'Do you have a physical office or storefront?',
      type: 'boolean'
    },
    {
      id: 'handlesCustomerData',
      question: 'Do you collect or store customer data?',
      type: 'boolean'
    },
    {
      id: 'hasBoard',
      question: 'Do you have a board of directors or outside investors?',
      type: 'boolean'
    },
    {
      id: 'providesAdvice',
      question: 'Do you provide professional advice or services to clients?',
      type: 'boolean'
    },
    {
      id: 'hasVehicles',
      question: 'Does your business own or use vehicles?',
      type: 'boolean'
    }
  ];

  const handleAnswer = (value) => {
    const currentQ = questions[step];
    setAnswers({ ...answers, [currentQ.id]: value });
    
    if (step < questions.length - 1) {
      setStep(step + 1);
    } else {
      setShowResults(true);
    }
  };

  const getRecommendations = () => {
    const recs = [];

    // General Liability - recommended for almost all businesses
    recs.push({
      name: 'General Liability Insurance',
      priority: 'Essential',
      reason: 'Protects against claims of bodily injury, property damage, and advertising injury. Required by most commercial leases and client contracts.',
      color: 'bg-red-50 border-red-200'
    });

    // Workers Compensation
    if (answers.employees !== '1-10' || answers.hasPhysicalLocation) {
      recs.push({
        name: 'Workers Compensation Insurance',
        priority: 'Essential',
        reason: 'Required by law in most states when you have employees. Covers medical costs and lost wages for work-related injuries.',
        color: 'bg-red-50 border-red-200'
      });
    }

    // Professional Liability
    if (answers.providesAdvice || ['Technology/SaaS', 'Professional Services', 'Financial Services'].includes(answers.industry)) {
      recs.push({
        name: 'Professional Liability Insurance (E&O)',
        priority: 'Essential',
        reason: 'Protects against claims of negligence, errors, or failure to deliver promised services. Critical for service-based businesses.',
        color: 'bg-red-50 border-red-200'
      });
    }

    // Cyber Liability
    if (answers.handlesCustomerData || ['Technology/SaaS', 'Healthcare', 'Financial Services', 'E-commerce/Retail'].includes(answers.industry)) {
      recs.push({
        name: 'Cyber Liability Insurance',
        priority: 'Highly Recommended',
        reason: 'Covers data breaches, ransomware attacks, and regulatory fines. Essential for any business handling customer data.',
        color: 'bg-orange-50 border-orange-200'
      });
    }

    // D&O
    if (answers.hasBoard || answers.revenue !== 'Under $1M') {
      recs.push({
        name: 'Directors & Officers (D&O) Insurance',
        priority: 'Highly Recommended',
        reason: 'Protects company leadership from personal liability for business decisions. Important for attracting board members and investors.',
        color: 'bg-orange-50 border-orange-200'
      });
    }

    // Commercial Property
    if (answers.hasPhysicalLocation) {
      recs.push({
        name: 'Commercial Property Insurance',
        priority: 'Recommended',
        reason: 'Covers damage to your building, equipment, and inventory from fire, theft, or natural disasters.',
        color: 'bg-blue-50 border-blue-200'
      });
    }

    // Business Interruption
    if (answers.revenue !== 'Under $1M' && answers.hasPhysicalLocation) {
      recs.push({
        name: 'Business Interruption Insurance',
        priority: 'Recommended',
        reason: 'Covers lost income and operating expenses if your business is forced to close temporarily due to a covered event.',
        color: 'bg-blue-50 border-blue-200'
      });
    }

    // Commercial Auto
    if (answers.hasVehicles) {
      recs.push({
        name: 'Commercial Auto Insurance',
        priority: 'Essential',
        reason: 'Required by law if your business owns vehicles. Covers accidents involving company vehicles.',
        color: 'bg-red-50 border-red-200'
      });
    }

    // Employment Practices Liability
    if (answers.employees !== '1-10') {
      recs.push({
        name: 'Employment Practices Liability (EPLI)',
        priority: 'Recommended',
        reason: 'Protects against claims of discrimination, wrongful termination, and harassment by employees.',
        color: 'bg-blue-50 border-blue-200'
      });
    }

    return recs;
  };

  const resetAssessment = () => {
    setStep(0);
    setAnswers({
      industry: '',
      employees: '',
      revenue: '',
      hasPhysicalLocation: null,
      handlesCustomerData: null,
      hasBoard: null,
      providesAdvice: null,
      hasVehicles: null
    });
    setShowResults(false);
  };

  if (showResults) {
    const recommendations = getRecommendations();
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex items-center gap-3 mb-6">
              <Shield className="w-8 h-8 text-indigo-600" />
              <h1 className="text-3xl font-bold text-gray-900">Your Insurance Recommendations</h1>
            </div>
            
            <div className="mb-8 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
              <p className="text-gray-700">Based on your responses, here are the insurance policies we recommend for your business:</p>
            </div>

            <div className="space-y-4 mb-8">
              {recommendations.map((rec, idx) => (
                <div key={idx} className={`border-2 ${rec.color} rounded-lg p-5`}>
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-semibold text-gray-900">{rec.name}</h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      rec.priority === 'Essential' ? 'bg-red-100 text-red-800' :
                      rec.priority === 'Highly Recommended' ? 'bg-orange-100 text-orange-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {rec.priority}
                    </span>
                  </div>
                  <p className="text-gray-700">{rec.reason}</p>
                </div>
              ))}
            </div>

            <div className="border-t pt-6">
              <div className="flex items-start gap-3 mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">
                  This assessment provides general guidance only. Every business is unique, and your specific needs may vary. Consult with an insurance professional for personalized advice.
                </p>
              </div>
              
              <button
                onClick={resetAssessment}
                className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
              >
                Start New Assessment
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const currentQ = questions[step];
  const progress = ((step + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="flex items-center gap-3 mb-8">
            <Building2 className="w-8 h-8 text-indigo-600" />
            <h1 className="text-3xl font-bold text-gray-900">Business Insurance Assessment</h1>
          </div>

          <div className="mb-8">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Question {step + 1} of {questions.length}</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">{currentQ.question}</h2>
            
            {currentQ.type === 'select' && (
              <div className="space-y-3">
                {currentQ.options.map((option) => (
                  <button
                    key={option}
                    onClick={() => handleAnswer(option)}
                    className="w-full text-left p-4 border-2 border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition-all"
                  >
                    <span className="text-lg text-gray-800">{option}</span>
                  </button>
                ))}
              </div>
            )}

            {currentQ.type === 'boolean' && (
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => handleAnswer(true)}
                  className="p-6 border-2 border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition-all"
                >
                  <span className="text-xl font-medium text-gray-800">Yes</span>
                </button>
                <button
                  onClick={() => handleAnswer(false)}
                  className="p-6 border-2 border-gray-200 rounded-lg hover:border-indigo-500 hover:bg-indigo-50 transition-all"
                >
                  <span className="text-xl font-medium text-gray-800">No</span>
                </button>
              </div>
            )}
          </div>

          {step > 0 && (
            <button
              onClick={() => setStep(step - 1)}
              className="text-indigo-600 hover:text-indigo-700 font-medium"
            >
              Back
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default InsuranceAssessment;
