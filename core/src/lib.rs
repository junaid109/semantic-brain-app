use pyo3::prelude::*;

/// A simple high-performance utility to test the bridge.
#[pyfunction]
fn calculate_relationship_weight(connections: u32, depth: u32) -> PyResult<f64> {
    // Custom logic that might be heavy in Python
    let weight = (connections as f64) * (0.5f64.powi(depth as i32));
    Ok(weight)
}

/// A Python module implemented in Rust.
#[pymodule]
fn semantic_brain_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_relationship_weight, m)?)?;
    Ok(())
}
