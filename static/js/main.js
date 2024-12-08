document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('transformForm');
    const results = document.getElementById('results');
    const loading = document.getElementById('loading');
    const resultsContent = document.getElementById('resultsContent');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading state
        results.classList.remove('hidden');
        loading.classList.remove('hidden');
        resultsContent.classList.add('hidden');
        
        const theme = document.getElementById('theme').value;
        
        try {
            const response = await fetch('/transform', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ theme }),
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Update the results
            updateResults(data);
            
            // Hide loading, show results
            loading.classList.add('hidden');
            resultsContent.classList.remove('hidden');
            
            // Scroll to results
            results.scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating your transformation plan. Please try again.');
            loading.classList.add('hidden');
        }
    });
});

function updateResults(data) {
    // Update summary
    document.getElementById('summary').textContent = data.summary;
    
    // Update color scheme
    const colorScheme = document.getElementById('colorScheme');
    colorScheme.innerHTML = '';
    
    const colors = [
        { color: data.color_scheme.primary, label: 'Primary' },
        { color: data.color_scheme.secondary, label: 'Secondary' },
        { color: data.color_scheme.accent1, label: 'Accent 1' },
        { color: data.color_scheme.accent2, label: 'Accent 2' },
    ];
    
    colors.forEach(({ color, label }) => {
        const swatch = document.createElement('div');
        swatch.className = 'color-swatch';
        swatch.style.backgroundColor = color;
        
        const labelDiv = document.createElement('div');
        labelDiv.className = 'text-center mt-2 text-sm text-gray-600';
        labelDiv.textContent = `${label}: ${color}`;
        
        const container = document.createElement('div');
        container.className = 'flex flex-col items-center';
        container.appendChild(swatch);
        container.appendChild(labelDiv);
        
        colorScheme.appendChild(container);
    });
    
    document.getElementById('colorDescription').textContent = data.color_scheme.description;
    
    // Update inspiration images
    const inspirationImages = document.getElementById('inspirationImages');
    inspirationImages.innerHTML = '';
    
    data.inspiration_images.forEach(image => {
        const imgContainer = document.createElement('div');
        imgContainer.className = 'relative';
        
        const img = document.createElement('img');
        img.src = image.url;
        img.alt = 'Interior design inspiration';
        img.className = 'inspiration-image w-full h-48 object-cover';
        
        const credit = document.createElement('div');
        credit.className = 'absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-xs p-2 text-center';
        credit.textContent = image.credit;
        
        imgContainer.appendChild(img);
        imgContainer.appendChild(credit);
        inspirationImages.appendChild(imgContainer);
    });
    
    // Update furniture list
    const furnitureList = document.getElementById('furniture');
    furnitureList.innerHTML = data.furniture.map(item => `
        <li class="text-gray-700">
            <span class="font-medium">${item.item}:</span> ${item.description}
        </li>
    `).join('');
    
    // Update lighting list
    const lightingList = document.getElementById('lighting');
    lightingList.innerHTML = data.lighting.map(item => `
        <li class="text-gray-700">
            <span class="font-medium">${item.type}:</span> ${item.purpose}
        </li>
    `).join('');
    
    // Update sensory elements
    const scentsList = document.getElementById('scents');
    scentsList.innerHTML = data.sensory.scents.map(scent => `
        <li>${scent}</li>
    `).join('');
    
    const soundsList = document.getElementById('sounds');
    soundsList.innerHTML = data.sensory.sounds.map(sound => `
        <li>${sound}</li>
    `).join('');
    
    // Update daily rituals
    const ritualsList = document.getElementById('dailyRituals');
    ritualsList.innerHTML = data.daily_rituals.map(ritual => `
        <li>${ritual}</li>
    `).join('');
}
