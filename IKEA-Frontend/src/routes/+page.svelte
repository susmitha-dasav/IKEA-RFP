<script lang="ts">
  import { onMount } from 'svelte';
  import { marked } from 'marked';

  let codebasePath = '';
  let isLoading = false;
  let error: string | null = null;
  let taskId: string | null = null;
  let status: string | null = null;
  let results: { documentation: string; summary: string } | null = null;

  const API_BASE_URL = 'http://localhost:8000';

  async function startAnalysis() {
    if (!codebasePath) {
      error = 'Please provide a codebase path.';
      return;
    }
    isLoading = true;
    error = null;
    results = null;
    taskId = null;
    status = 'Submitting...';

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ codebase_path: codebasePath }),
      });

      if (!response.ok) {
        throw new Error(`Failed to start analysis. Server responded with ${response.status}`);
      }

      const data = await response.json();
      taskId = data.task_id;
      status = data.status;
      pollStatus();
    } catch (e: any) {
      error = e.message;
      isLoading = false;
    }
  }

  async function pollStatus() {
    if (!taskId) return;

    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/status/${taskId}`);
        if (!response.ok) {
          throw new Error('Failed to get status.');
        }
        const data = await response.json();
        status = data.details;

        if (data.status === 'completed') {
          clearInterval(interval);
          await fetchResults();
        } else if (data.status === 'failed') {
          clearInterval(interval);
          error = `Analysis failed: ${data.details}`;
          isLoading = false;
        }
      } catch (e: any) {
        error = e.message;
        isLoading = false;
        clearInterval(interval);
      }
    }, 2000); // Poll every 2 seconds
  }

  async function fetchResults() {
    if (!taskId) return;
    try {
      console.log(await marked.parse('# My title'))
      const response = await fetch(`${API_BASE_URL}/results/${taskId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch results.');
      }
      const data = await response.json();
      results = {
        summary: await marked.parse(data.results.summary),
        documentation: await marked.parse(data.results.documentation)
      };
    } catch (e: any) {
      error = e.message;
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen bg-gray-100 text-gray-900 p-4 sm:p-6 lg:p-8">
  <div class="max-w-4xl mx-auto">
    <header class="text-center mb-8">
      <h1 class="text-3xl font-bold text-blue-700">AutoGen PL/SQL Analyzer</h1>
      <p class="text-gray-600">Reverse-engineer your PL/SQL codebase with the power of AI agents.</p>
    </header>

    <!-- Input Panel -->
    <div class="bg-white p-6 rounded-lg shadow-md mb-8">
      <h2 class="text-xl font-semibold mb-4">Codebase Analysis</h2>
      <div class="flex items-center">
        <input
          type="text"
          bind:value={codebasePath}
          placeholder="Enter absolute path to your PL/SQL codebase"
          class="flex-grow p-2 border rounded-l-md focus:ring-blue-500 focus:border-blue-500"
          disabled={isLoading}
        />
        <button 
          on:click={startAnalysis}
          class="bg-blue-600 text-white px-4 py-2 rounded-r-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400"
          disabled={isLoading}
        >
          {#if isLoading}
            <span>Analyzing...</span>
          {:else}
            <span>Start Analysis</span>
          {/if}
        </button>
      </div>
    </div>

    <!-- Status and Error Display -->
    {#if error}
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md relative mb-6" role="alert">
        <strong class="font-bold">Error:</strong>
        <span class="block sm:inline">{error}</span>
      </div>
    {/if}

    {#if isLoading}
      <div class="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 class="text-xl font-semibold mb-4">Analysis in Progress</h2>
        <div class="flex items-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
          <p class="text-gray-600">{status || 'Initializing...'}</p>
        </div>
      </div>
    {/if}

    <!-- Output Panel -->
    {#if results}
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold mb-4">Results</h2>
        
        <div class="prose max-w-none mb-8">
            <h3 class="text-lg font-semibold">Codebase Summary</h3>
            {@html results.summary}
        </div>

        <hr class="my-6">

        <div class="prose max-w-none">
            <h3 class="text-lg font-semibold">Detailed Documentation</h3>
            {@html results.documentation}
        </div>
      </div>
    {/if}
  </div>
</div>

