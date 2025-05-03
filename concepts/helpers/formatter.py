def FormatDiagnosis(diagnosis_dict):
  match (diagnosis_dict["adhd"], diagnosis_dict["spectrum"]):
    case (True, True):
      status = "ADHD and autism spectrum"
    case (True, False):
      status = "ADHD"
    case (False, True):
      status = "autism spectrum"
  return status