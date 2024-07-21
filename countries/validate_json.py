import json
import os
from jsonschema import validate, ValidationError
from pathlib import Path

# Define the JSON schema based on your template
schema = {
    "type": "object",
    "properties": {
        "country_name": {"type": "string"},
        "country_code": {"type": "string"},
        "capital": {"type": "string"},
        "display": {"type": "boolean"},
        "currency": {"type": "string"},
        "anchor_country": {"type": "boolean"},
        "has_nomad_visa": {"type": "boolean"},
        "schengen_zone": {"type": "boolean"},
        "in_european_union": {"type": "boolean"},
        "cost_of_living_index": {"type": "number"},
        "cost_of_living_lvl": {"type": "string"},
        "practical_tips": {
            "type": "object",
            "properties": {
                "financial_benefits": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "properties": {
                            "benefit": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["benefit", "description"]
                    }
                },
                "lifestyle_benefits": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "properties": {
                            "benefit": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["benefit", "description"]
                    }
                },
                "additional_benefits": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "properties": {
                            "benefit": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["benefit", "description"]
                    }
                }
            },
            "required": ["financial_benefits", "lifestyle_benefits", "additional_benefits"]
        },
        "key_consideration": {"type": "string"},
        "best_for": {"type": "array", "items": {"type": "string"}},
        "action_comment": {"type": "string"},
        "tagline": {"type": "string"},
        "image": {"type": "string"},
        "tax_residency_trigger": {"type": "integer"},
        "tax_residency_trigger_details": {"type": "string"},
        "country_standard_taxes": {
            "type": "object",
            "properties": {
                "tax_currency": {"type": "string"},
                "employees": {
                    "type": "object",
                    "properties": {
                        "income_tax": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "min_income_range": {"type": "number"},
                                    "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                    "rate_pct": {"type": "number"}
                                },
                                "required": ["min_income_range", "max_income_range", "rate_pct"]
                            }
                        },
                        "social_security": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "min_income_range": {"type": "number"},
                                    "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                    "rate_pct": {"type": "number"},
                                    "misc_details": {"type": "string"}
                                },
                                "required": ["min_income_range", "max_income_range", "rate_pct"]
                            }
                        }
                    },
                    "required": ["income_tax", "social_security"]
                },
                "contractors": {
                    "type": "object",
                    "properties": {
                        "income_tax": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "min_income_range": {"type": "number"},
                                    "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                    "rate_pct": {"type": "number"}
                                },
                                "required": ["min_income_range", "max_income_range", "rate_pct"]
                            }
                        },
                        "social_security": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "min_income_range": {"type": "number"},
                                    "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                    "rate_pct": {"type": "number"},
                                    "misc_details": {"type": "string"}
                                },
                                "required": ["min_income_range", "max_income_range", "rate_pct"]
                            }
                        }
                    },
                    "required": ["income_tax", "social_security"]
                },
                "retirees": {
                    "type": "object",
                    "properties": {
                        "income_tax": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "min_income_range": {"type": "number"},
                                    "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                    "rate_pct": {"type": "number"}
                                },
                                "required": ["min_income_range", "max_income_range", "rate_pct"]
                            }
                        },
                        "social_security": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "min_income_range": {"type": "number"},
                                    "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                    "rate_pct": {"type": "number"},
                                    "misc_details": {"type": "string"}
                                },
                                "required": ["min_income_range", "max_income_range", "rate_pct"]
                            }
                        }
                    },
                    "required": ["income_tax", "social_security"]
                }
            },
            "required": ["tax_currency", "employees", "contractors", "retirees"]
        },
        "visas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "visa_name": {"type": "string"},
                    "nomad_visa": {"type": "boolean"},
                    "official_government_link": {"type": "string"},
                    "key_consideration": {"type": "string"},
                    "validity_months": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                    "income_requirement": {
                        "type": "object",
                        "properties": {
                            "currency": {"type": "string"},
                            "single_monthly": {"type": "number"},
                            "family_monthly": {"type": "number"},
                            "misc_details": {"type": "string"}
                        },
                        "required": ["currency", "single_monthly"]
                    },
                    "application_timeline_days": {"type": "integer"},
                    "application_in_country": {"type": "boolean"},
                    "application_fee": {
                        "type": "object",
                        "properties": {
                            "currency": {"type": "string"},
                            "single": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                            "family": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                            "details": {"type": "string"}
                        },
                        "required": ["currency", "single"]
                    },
                    "dependent_application": {"type": "boolean"},
                    "local_tax_on_foreign_income": {"type": "boolean"},
                    "renewability": {"type": "boolean"},
                    "renewability_details": {"type": "string"},
                    "days_in_country_to_renew_visa": {"type": "integer"},
                    "special_tax_regime": {"type": "boolean"},
                    "special_tax_regime_details": {"type": "string"},
                    "leads_to_permanent_residence": {"type": "boolean"},
                    "permanent_residency_details": {"type": "string"},
                    "taxes": {
                        "type": "object",
                        "properties": {
                            "employees": {
                                "type": "object",
                                "properties": {
                                    "income_tax": {"type": "array", "items": {"type": "object"}},
                                    "social_security": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "min_income_range": {"type": "number"},
                                                "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                                "rate_pct": {"type": "number"},
                                                "misc_details": {"type": "string"}
                                            },
                                            "required": ["min_income_range", "max_income_range", "rate_pct"]
                                        }
                                    }
                                },
                                "required": ["income_tax", "social_security"]
                            },
                            "contractors": {
                                "type": "object",
                                "properties": {
                                    "income_tax": {"type": "array", "items": {"type": "object"}},
                                    "social_security": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "min_income_range": {"type": "number"},
                                                "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                                "rate_pct": {"type": "number"},
                                                "misc_details": {"type": "string"}
                                            },
                                            "required": ["min_income_range", "max_income_range", "rate_pct"]
                                        }
                                    }
                                },
                                "required": ["income_tax", "social_security"]
                            },
                            "retirees": {
                                "type": "object",
                                "properties": {
                                    "income_tax": {"type": "array", "items": {"type": "object"}},
                                    "social_security": {"type": "array", "items": {"type": "object"}}
                                },
                                "required": ["income_tax", "social_security"]
                            },
                            "special_regimes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "benefit": {"type": "string"},
                                        "eligibility": {"type": "array", "items": {"type": "string"}},
                                        "contractors_with_foreign_clients_eligible": {"type": "boolean"},
                                        "contractors_with_local_clients_eligible": {"type": "boolean"},
                                        "employees_with_foreign_employer_eligible": {"type": "boolean"},
                                        "apply_standard_rate_after_trigger": {"type": "boolean"},
                                        "apply_special_rate_after_trigger": {"type": "boolean"},
                                        "social_security": {
                                            "anyOf": [
                                                {"type": "boolean"},
                                                {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "min_income_range": {"type": "number"},
                                                            "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                                            "rate_pct": {"type": "number"},
                                                            "misc_details": {"type": "string"}
                                                        },
                                                        "required": ["min_income_range", "max_income_range", "rate_pct"]
                                                    }
                                                }
                                            ]
                                        },
                                        "income_tax": {
                                            "anyOf": [
                                                {"type": "boolean"},
                                                {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "min_income_range": {"type": "number"},
                                                            "max_income_range": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                                                            "rate_pct": {"type": "number"},
                                                            "misc_details": {"type": "string"}
                                                        },
                                                        "required": ["min_income_range", "max_income_range", "rate_pct"]
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    "required": ["name", "apply_special_rate_after_trigger", "apply_standard_rate_after_trigger", "benefit", "eligibility", "contractors_with_foreign_clients_eligible", "contractors_with_local_clients_eligible", "employees_with_foreign_employer_eligible", "social_security", "income_tax"]
                                }
                            }
                        },
                        "required": ["employees", "contractors", "retirees", "special_regimes"]
                    },
                    "required_documents": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["visa_name", "nomad_visa", "key_consideration", "special_tax_regime"],
                "if": {
                    "properties": {
                        "nomad_visa": {
                            "const": False
                        }
                    }
                },
                "then": {
                    "required": ["visa_name"]
                }
            }
        }
    },
    "required": [
        "country_name", "country_code", "capital", "display", "currency", "anchor_country", "has_nomad_visa",
        "schengen_zone", "in_european_union", "cost_of_living_index", "cost_of_living_lvl", "practical_tips",
        "key_consideration", "best_for", "action_comment", "tagline", "image", "tax_residency_trigger",
        "tax_residency_trigger_details", "country_standard_taxes", "visas"
    ]
}

def validate_json_files(directory):
    json_files = Path(directory).glob('*.json')
    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                json_data = json.load(file)
                validate(instance=json_data, schema=schema)
        except ValidationError as e:
            error_message = f"{json_file.name}: Invalid JSON\n"
            error_message += f"'{e.message}' (path: {'/'.join(map(str, e.path))})\n"
            error_message += f"'{e.message}'\n\n"
            print(error_message.strip())
        except json.JSONDecodeError as e:
            print(f"{json_file.name}: Error decoding JSON. Error: {e.msg} on line {e.lineno}\n")

# Specify the directory containing the JSON files
directory = "/Users/erickufta/Projects/admin-wealthy-wanderers/countries/07:20:2024"
validate_json_files(directory)
