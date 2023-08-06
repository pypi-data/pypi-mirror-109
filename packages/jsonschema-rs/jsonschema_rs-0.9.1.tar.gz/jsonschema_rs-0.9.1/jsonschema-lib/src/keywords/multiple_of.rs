use crate::{
    compilation::{context::CompilationContext, JSONSchema},
    error::{error, no_error, CompilationError, ErrorIterator, ValidationError},
    keywords::CompilationResult,
    paths::InstancePath,
    validator::Validate,
};
use fraction::{BigFraction, BigUint};
use serde_json::{Map, Value};
use std::f64::EPSILON;

pub(crate) struct MultipleOfFloatValidator {
    multiple_of: f64,
}

impl MultipleOfFloatValidator {
    #[inline]
    pub(crate) fn compile(multiple_of: f64) -> CompilationResult {
        Ok(Box::new(MultipleOfFloatValidator { multiple_of }))
    }
}

impl Validate for MultipleOfFloatValidator {
    fn is_valid(&self, _: &JSONSchema, instance: &Value) -> bool {
        if let Value::Number(item) = instance {
            let item = item.as_f64().expect("Always valid");
            let remainder = (item / self.multiple_of) % 1.;
            if remainder.is_nan() {
                // Involves heap allocations via the underlying `BigUint` type
                let fraction = BigFraction::from(item) / BigFraction::from(self.multiple_of);
                if let Some(denom) = fraction.denom() {
                    return denom == &BigUint::from(1_u8);
                }
            } else if !(remainder < EPSILON && remainder < (1. - EPSILON)) {
                return false;
            }
        }
        true
    }

    fn validate<'a>(
        &self,
        schema: &'a JSONSchema,
        instance: &'a Value,
        instance_path: &InstancePath,
    ) -> ErrorIterator<'a> {
        if !self.is_valid(schema, instance) {
            return error(ValidationError::multiple_of(
                instance_path.into(),
                instance,
                self.multiple_of,
            ));
        }
        no_error()
    }
}

impl ToString for MultipleOfFloatValidator {
    fn to_string(&self) -> String {
        format!("multipleOf: {}", self.multiple_of)
    }
}

pub(crate) struct MultipleOfIntegerValidator {
    multiple_of: f64,
}

impl MultipleOfIntegerValidator {
    #[inline]
    pub(crate) fn compile(multiple_of: f64) -> CompilationResult {
        Ok(Box::new(MultipleOfIntegerValidator { multiple_of }))
    }
}

impl Validate for MultipleOfIntegerValidator {
    fn is_valid(&self, _: &JSONSchema, instance: &Value) -> bool {
        if let Value::Number(item) = instance {
            let item = item.as_f64().expect("Always valid");
            let is_multiple = if item.fract() == 0. {
                (item % self.multiple_of) == 0.
            } else {
                let remainder = (item / self.multiple_of) % 1.;
                remainder < EPSILON && remainder < (1. - EPSILON)
            };
            if !is_multiple {
                return false;
            }
        }
        true
    }

    fn validate<'a>(
        &self,
        schema: &'a JSONSchema,
        instance: &'a Value,
        instance_path: &InstancePath,
    ) -> ErrorIterator<'a> {
        if !self.is_valid(schema, instance) {
            return error(ValidationError::multiple_of(
                instance_path.into(),
                instance,
                self.multiple_of,
            ));
        }
        no_error()
    }
}

impl ToString for MultipleOfIntegerValidator {
    fn to_string(&self) -> String {
        format!("multipleOf: {}", self.multiple_of)
    }
}
#[inline]
pub(crate) fn compile(
    _: &Map<String, Value>,
    schema: &Value,
    _: &CompilationContext,
) -> Option<CompilationResult> {
    if let Value::Number(multiple_of) = schema {
        let multiple_of = multiple_of.as_f64().expect("Always valid");
        if multiple_of.fract() == 0. {
            Some(MultipleOfIntegerValidator::compile(multiple_of))
        } else {
            Some(MultipleOfFloatValidator::compile(multiple_of))
        }
    } else {
        Some(Err(CompilationError::SchemaError))
    }
}
