import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import api from '@/services/api'; // Import your API service
import { discoveryengine_v1beta } from '@google-cloud/discoveryengine'; // For type mocking

// Mock the Gemini API client
const mockConverseConversation = vi.fn();
const mockGeminiClient = {
    converseConversation: mockConverseConversation,
} as discoveryengine_v1beta.ConversationalSearchServiceClient;

vi.mock('@google-cloud/discoveryengine', () => ({
    discoveryengine_v1beta: {
        ConversationalSearchServiceClient: vi.fn(() => mockGeminiClient),
        // ... mock other necessary parts of the Gemini library
    },
}));



describe('api.generateNarrative', () => {

    beforeEach(() => {
        mockConverseConversation.mockResolvedValue({  // Mock a successful response
            reply: { text: 'This is a mock generated narrative.' },
        });
    })

    afterEach(() => {
        vi.clearAllMocks(); //Clear all mocks to ensure independence
    })



  it('should call the Gemini API with the correct prompt', async () => {
    const prompt = 'Write a story about a cat.';
    await api.generateNarrative(prompt);

    expect(mockConverseConversation).toHaveBeenCalledWith(expect.objectContaining({
        query: { text: prompt },
    }));


  });

  it('should return the generated narrative on success', async () => {

    const narrative = await api.generateNarrative('Test prompt');
    expect(narrative).toBe('This is a mock generated narrative.');
  });


  it('should handle errors from the Gemini API', async () => {
    const errorMessage = 'Gemini API error';
    mockConverseConversation.mockRejectedValueOnce(new Error(errorMessage)); // Mock an error

    try{
        await api.generateNarrative('Error test prompt');
    }
    catch(error){

        expect(error).toEqual(new Error(errorMessage))
    }



  });
});