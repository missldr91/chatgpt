// Test upload functionality
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const API_URL = 'https://8000-ieq6xwbj6bsk4tk4gpuij-6532622b.e2b.dev';
const templatePath = '/home/user/webapp/app/svc/data/fixtures/templates/brand_simple.pptx';

async function testUpload() {
  try {
    const form = new FormData();
    form.append('file', fs.createReadStream(templatePath));
    
    const response = await axios.post(`${API_URL}/templates/ingest`, form, {
      headers: {
        ...form.getHeaders(),
        'Origin': 'https://3000-ieq6xwbj6bsk4tk4gpuij-6532622b.e2b.dev'
      }
    });
    
    console.log('✅ Upload successful!');
    console.log('Template ID:', response.data.template_id);
    console.log('Layouts found:', response.data.layout_catalog.length);
  } catch (error) {
    console.error('❌ Upload failed:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', error.response.data);
    }
  }
}

testUpload();