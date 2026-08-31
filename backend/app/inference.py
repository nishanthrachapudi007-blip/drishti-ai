from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

LABELS=["No DR","Mild NPDR","Moderate NPDR","Severe NPDR","Proliferative DR"]
@dataclass(frozen=True)
class InferenceResult:
    predicted_class:int; probabilities:list[float]; method:str; summary:str; artifact_path:str|None=None; is_demo:bool=True
class InferenceService(ABC):
    @abstractmethod
    async def predict(self,image_path:Path)->InferenceResult: ...
class DemoInferenceService(InferenceService):
    """Fixed UI-development output. Never use for clinical decisions or benchmarking."""
    async def predict(self,image_path:Path)->InferenceResult:
        return InferenceResult(2,[0.03,0.06,0.87,0.03,0.01],"illustrative-overlay","Fixed demo output; highlighted regions are illustrative and not derived from medical evidence.")
class TorchInferenceService(InferenceService):
    def __init__(self,model_path:Path):
        if not model_path.exists(): raise FileNotFoundError(model_path)
        raise NotImplementedError("Implement preprocessing, validated checkpoint loading, calibration, and Grad-CAM for the selected trained model.")
def get_inference_service(provider:str="demo",model_path:str|None=None)->InferenceService:
    if provider=="demo": return DemoInferenceService()
    if provider=="torch" and model_path: return TorchInferenceService(Path(model_path))
    raise RuntimeError("A configured inference provider and model path are required")

