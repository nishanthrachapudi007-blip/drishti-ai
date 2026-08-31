# ML integration boundary

No trained model or dataset mapping is included. The backend uses `DemoInferenceService`, which returns a fixed, clearly labelled result for UI development.

To integrate a real model, implement `TorchInferenceService` with the exact preprocessing used during training, load a versioned and integrity-checked checkpoint, return calibrated five-class probabilities, and generate a clinically reviewed explainability artifact. Validate on the documented dataset split before enabling non-demo mode. APTOS and mBRSET must retain their own documented label semantics and must never be merged through inferred filenames or folder names.

