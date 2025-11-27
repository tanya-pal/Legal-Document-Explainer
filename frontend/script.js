// Global variables
let currentAnalysis = null;
let currentClauses = [];
let currentText = '';

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const progressFill = document.getElementById('progressFill');
const scoreNumber = document.getElementById('scoreNumber');
const riskBreakdown = document.getElementById('riskBreakdown');
const summaryContent = document.getElementById('summaryContent');
const clausesList = document.getElementById('clausesList');
const originalText = document.getElementById('originalText');
const sidePanel = document.getElementById('sidePanel');
const overlay = document.getElementById('overlay');
const sidePanelTitle = document.getElementById('sidePanelTitle');
const sidePanelContent = document.getElementById('sidePanelContent');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    setupDragAndDrop();
});

// Initialize event listeners
function initializeEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Analyze button
    analyzeBtn.addEventListener('click', analyzeDocument);
    
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            filterClauses(this.dataset.filter);
        });
    });
    
    // Close side panel on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSidePanel();
        }
    });
}

// Setup drag and drop functionality
function setupDragAndDrop() {
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Handle file processing
function handleFile(file) {
    // Validate file type
    const allowedTypes = ['application/pdf', 'text/plain'];
    if (!allowedTypes.includes(file.type) && !file.name.endsWith('.pdf') && !file.name.endsWith('.txt')) {
        showError('Please select a PDF or text file.');
        return;
    }
    
    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB.');
        return;
    }
    
    // Display file info
    displayFileInfo(file);
}

// Display file information
function displayFileInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    uploadArea.style.display = 'none';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Analyze document
async function analyzeDocument() {
    const file = fileInput.files[0];
    if (!file) {
        showError('Please select a file first.');
        return;
    }
    
    try {
        // Show loading state
        showLoading();
        
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        
        // Simulate progress
        simulateProgress();
        
        // Send request to backend
        const response = await fetch('/analyze_document', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Store current analysis
        currentAnalysis = result;
        currentClauses = result.analysis.clauses;
        currentText = result.upload_info.text_content;
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error analyzing document:', error);
        showError('An error occurred while analyzing the document. Please try again.');
    } finally {
        hideLoading();
    }
}

// Show loading state
function showLoading() {
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
}

// Hide loading state
function hideLoading() {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
}

// Simulate progress bar
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) {
            progress = 90;
            clearInterval(interval);
        }
        progressFill.style.width = progress + '%';
    }, 200);
}

// Display analysis results
function displayResults(result) {
    // Display risk score
    displayRiskScore(result.risk_assessment);
    
    // Display summary
    displaySummary(result.analysis.summary);
    
    // Display clauses
    displayClauses(result.analysis.clauses);
    
    // Display original text with highlights
    displayOriginalText(result.upload_info.text_content, result.analysis.clauses);
}

// Display risk score
function displayRiskScore(riskAssessment) {
    scoreNumber.textContent = riskAssessment.score;
    
    // Update score circle color based on risk level
    const scoreCircle = document.querySelector('.score-circle');
    if (riskAssessment.score >= 70) {
        scoreCircle.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    } else if (riskAssessment.score >= 40) {
        scoreCircle.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    } else {
        scoreCircle.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
    }
    
    // Display risk breakdown
    displayRiskBreakdown(riskAssessment.breakdown);
}

// Display risk breakdown
function displayRiskBreakdown(breakdown) {
    riskBreakdown.innerHTML = '';
    
    Object.entries(breakdown).forEach(([type, score]) => {
        const riskItem = document.createElement('div');
        riskItem.className = 'risk-item';
        
        const riskLevel = score > 30 ? 'high' : score > 15 ? 'medium' : 'low';
        riskItem.classList.add(riskLevel);
        
        riskItem.innerHTML = `
            <div class="flex justify-between items-center">
                <span class="font-semibold">${formatClauseType(type)}</span>
                <span class="text-sm">${score} points</span>
            </div>
        `;
        
        riskBreakdown.appendChild(riskItem);
    });
}

// Display summary
function displaySummary(summary) {
    summaryContent.textContent = summary;
}

// Display clauses
function displayClauses(clauses) {
    clausesList.innerHTML = '';
    
    if (clauses.length === 0) {
        clausesList.innerHTML = '<p class="text-gray-500 text-center py-4">No clauses identified in this document.</p>';
        return;
    }
    
    clauses.forEach((clause, index) => {
        const clauseItem = document.createElement('div');
        clauseItem.className = `clause-item ${clause.risk_level}`;
        clauseItem.dataset.index = index;
        
        clauseItem.innerHTML = `
            <div class="clause-header">
                <span class="clause-type">${formatClauseType(clause.type)}</span>
                <span class="clause-risk ${clause.risk_level}">${clause.risk_level}</span>
            </div>
            <div class="clause-text">${clause.text}</div>
        `;
        
        clauseItem.addEventListener('click', () => showClauseDetails(clause));
        clausesList.appendChild(clauseItem);
    });
}

// Display original text with highlights
function displayOriginalText(text, clauses) {
    let highlightedText = text;
    
    // Sort clauses by start index in reverse order to avoid index shifting
    const sortedClauses = [...clauses].sort((a, b) => b.start_index - a.start_index);
    
    sortedClauses.forEach((clause, index) => {
        const start = clause.start_index;
        const end = clause.end_index;
        const clauseText = text.substring(start, end);
        
        const highlightClass = `highlight ${clause.risk_level}`;
        const highlightedClause = `<span class="${highlightClass}" data-clause-index="${index}">${clauseText}</span>`;
        
        highlightedText = highlightedText.substring(0, start) + highlightedClause + highlightedText.substring(end);
    });
    
    originalText.innerHTML = highlightedText;
    
    // Add click listeners to highlights
    originalText.querySelectorAll('.highlight').forEach(highlight => {
        highlight.addEventListener('click', function() {
            const index = parseInt(this.dataset.clauseIndex);
            showClauseDetails(clauses[index]);
        });
    });
}

// Show clause details in side panel
function showClauseDetails(clause) {
    sidePanelTitle.textContent = formatClauseType(clause.type);
    
    sidePanelContent.innerHTML = `
        <div class="mb-3">
            <div class="flex items-center gap-2 mb-2">
                <span class="clause-risk ${clause.risk_level}">${clause.risk_level}</span>
                <span class="text-sm text-gray-500">Risk Level</span>
            </div>
        </div>
        
        <div class="mb-4">
            <h4 class="font-semibold mb-2">Clause Text</h4>
            <div class="bg-gray-50 p-3 rounded border text-sm">
                ${clause.text}
            </div>
        </div>
        
        <div class="mb-4">
            <h4 class="font-semibold mb-2">Explanation</h4>
            <p class="text-gray-700">${clause.explanation}</p>
        </div>
        
        <div class="mb-4">
            <h4 class="font-semibold mb-2">Recommendations</h4>
            <ul class="list-disc list-inside text-sm text-gray-700 space-y-1">
                <li>Review this clause carefully before signing</li>
                <li>Consider consulting a legal professional</li>
                <li>Understand the implications for your rights</li>
            </ul>
        </div>
    `;
    
    openSidePanel();
}

// Open side panel
function openSidePanel() {
    sidePanel.classList.add('open');
    overlay.classList.add('active');
}

// Close side panel
function closeSidePanel() {
    sidePanel.classList.remove('open');
    overlay.classList.remove('active');
}

// Filter clauses
function filterClauses(filter) {
    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filter clauses
    const clauseItems = document.querySelectorAll('.clause-item');
    clauseItems.forEach(item => {
        if (filter === 'all' || item.classList.contains(filter)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Format clause type for display
function formatClauseType(type) {
    return type.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

// Show error message
function showError(message) {
    // Create error notification
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Close modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('active');
}

// Utility function to show modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('active');
}

// Export functions for global access
window.closeSidePanel = closeSidePanel;
window.closeModal = closeModal; 