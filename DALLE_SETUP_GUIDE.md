# DALL-E 3 REST API Setup Guide for Indian Region

## Overview
This guide helps you configure DALL-E 3 image generation using direct REST API calls, perfect for Indian region deployments.

## Configuration Options

### Option 1: Standard OpenAI API (Recommended)
**Best for**: Global access including India

1. Get your API key from: https://platform.openai.com/api-keys
2. Update `.env` file:
```env
DALLE_API_ENDPOINT=https://api.openai.com/v1/images/generations
DALLE_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
DALLE_MODEL=dall-e-3
```

### Option 2: Azure OpenAI with DALL-E 3
**Best for**: If your Azure region supports DALL-E (East US, Sweden Central, Australia East)

1. Deploy DALL-E 3 model in Azure OpenAI Studio
2. Update `.env` file:
```env
DALLE_API_ENDPOINT=https://YOUR-RESOURCE-NAME.openai.azure.com/openai/deployments/YOUR-DALLE-DEPLOYMENT-NAME/images/generations?api-version=2024-02-01
DALLE_API_KEY=your-azure-openai-key
DALLE_MODEL=dall-e-3
```

**Note**: Replace:
- `YOUR-RESOURCE-NAME` with your Azure OpenAI resource name
- `YOUR-DALLE-DEPLOYMENT-NAME` with your DALL-E deployment name
- `your-azure-openai-key` with your Azure OpenAI API key

### Option 3: Custom DALL-E Endpoint
**Best for**: Enterprise/custom deployments

```env
DALLE_API_ENDPOINT=https://your-custom-endpoint.com/v1/images/generations
DALLE_API_KEY=your-custom-api-key
DALLE_MODEL=dall-e-3
```

## How It Works

The system uses **REST API calls** instead of SDK:

1. **Priority 1**: DALL-E REST API (configured endpoint)
2. **Priority 2**: Azure OpenAI SDK fallback
3. **Priority 3**: Standard OpenAI SDK fallback
4. **Priority 4**: High-quality stock images

## Testing Your Configuration

1. Update `.env` with your chosen option above
2. Restart the app:
```bash
python app.py
```

3. Create a campaign with social media posts
4. Check terminal output for:
```
🎨 Generating campaign-specific image for facebook...
🔹 Using DALL-E 3 REST API (configured endpoint)...
🌐 Endpoint: https://api.openai.com/v1/images/generations
🔹 Making REST API call to DALL-E 3...
✅ Successfully generated image with DALL-E 3 (REST API)
```

## Indian Region Notes

- **Standard OpenAI API works globally** including India
- **Azure OpenAI availability**: Check if DALL-E is available in your Azure region
  - Available: East US, Sweden Central, Australia East
  - Not available yet: India Central, India South
- **Latency**: Standard OpenAI may have 200-500ms latency from India
- **Fallback**: If DALL-E fails, high-quality stock images are used automatically

## Troubleshooting

### Issue: "DALL-E 3 REST API failed (Status 401)"
**Solution**: Check your API key in `.env` file

### Issue: "DALL-E 3 REST API timeout"
**Solution**: Network issue or endpoint down. Will auto-fallback to stock images

### Issue: "Model not supported in this region"
**Solution**: 
- For Azure: Use a supported region or standard OpenAI
- For Standard OpenAI: Should work globally

### Issue: "No images generating"
**Solution**: Check terminal output for specific error messages

## Cost Estimation

**DALL-E 3 Pricing** (Standard OpenAI):
- Standard quality (1024x1024): $0.040 per image
- HD quality (1024x1024): $0.080 per image

**Example**:
- 3 social media posts × 1 image each = 3 images
- Cost: 3 × $0.040 = $0.12 per campaign

## Support

For issues or questions:
1. Check terminal output for detailed error messages
2. Verify endpoint URL format matches your provider
3. Test API key with curl:

```bash
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A beautiful sunset",
    "n": 1,
    "size": "1024x1024"
  }'
```
