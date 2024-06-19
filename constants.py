MAX_RECURSION_DEPTH = 5

PRIMITIVE_KIND = "primitive-type"
COMPLEX_KIND = "complex-type"

PRIMITIVE_ELEMENT_TYPES = [
    "base64Binary",
    "boolean",
    "canonical",
    "code",
    "date",
    "dateTime",
    "decimal",
    "id",
    "instant",
    "integer",
    "integer64",
    "markdown",
    "oid",
    "positiveInt",
    "string",
    "http://hl7.org/fhirpath/System.String",  # This is a special case
    "time",
    "unsignedInt",
    "uri",
    "url",
    "uuid",
    "xhtml",
]

COMPLEX_ELEMENT_TYPES = [
    "Address",
    "Age",
    "Annotation",
    "Attachment",
    "BackboneElement",
    "CodeableConcept",
    "Coding",
    "ContactDetail",
    "ContactPoint",
    "Contributor",
    "Count",
    "DataRequirement",
    "Distance",
    "Dosage",
    "Duration",
    "Element",
    "ElementDefinition",
    "Expression",
    "Extension",
    "HumanName",
    "Identifier",
    "MarketingStatus",
    "Meta",
    "Money",
    "MoneyQuantity",
    "Narrative",
    "ParameterDefinition",
    "Period",
    "Population",
    "ProdCharacteristic",
    "ProductShelfLife",
    "Quantity",
    "Range",
    "Ratio",
    "Reference",
    "RelatedArtifact",
    "SampledData",
    "Signature",
    "SimpleQuantity",
    "SubstanceAmount",
    "Timing",
    "TriggerDefinition",
    "UsageContext",
]

CONTAINED_ELEMENT_TYPES = ["Resource", "DomainResource", "BackboneElement", "Element"]
