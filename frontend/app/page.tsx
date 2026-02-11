'use client'

import { useState } from 'react'
import SubmitApplication from '@/components/SubmitApplication'
import ReviewWorkflow from '@/components/ReviewWorkflow'
import WorkflowsList from '@/components/WorkflowsList'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'submit' | 'review' | 'workflows'>('submit')

  return (
    <main className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-green-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🏦 AI Loan Underwriter Pro
          </h1>
          <p className="text-lg text-gray-600">
            Powered by AWS Bedrock Nova + Temporal Workflows | By Norvin Samson Anthony
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('submit')}
                className={`flex-1 py-4 px-6 text-center font-medium text-sm transition-colors ${
                  activeTab === 'submit'
                    ? 'border-b-2 border-emerald-500 text-emerald-600 bg-emerald-50'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                📝 Submit Application
              </button>
              <button
                onClick={() => setActiveTab('review')}
                className={`flex-1 py-4 px-6 text-center font-medium text-sm transition-colors ${
                  activeTab === 'review'
                    ? 'border-b-2 border-emerald-500 text-emerald-600 bg-emerald-50'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                👨‍💼 Review Loan
              </button>
              <button
                onClick={() => setActiveTab('workflows')}
                className={`flex-1 py-4 px-6 text-center font-medium text-sm transition-colors ${
                  activeTab === 'workflows'
                    ? 'border-b-2 border-emerald-500 text-emerald-600 bg-emerald-50'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                📊 All Workflows
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'submit' && <SubmitApplication />}
            {activeTab === 'review' && <ReviewWorkflow />}
            {activeTab === 'workflows' && <WorkflowsList />}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-600">
          <p>
            Architecture: Temporal (Orchestration) + LangChain (Agents) + AWS Bedrock (AI Models) + MCP (Tools)
          </p>
        </div>
      </div>
    </main>
  )
}
