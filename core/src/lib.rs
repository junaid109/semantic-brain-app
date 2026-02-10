use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct NodeInfo {
    pub id: String,
    pub weight: f64,
}

/// Computes a decayed relevance score for a multi-hop relationship path.
/// Formula: sum(edge_weights) * (relevance_decay ^ hop_count)
#[pyfunction]
fn score_relationship_path(edge_weights: Vec<f64>, decay_factor: f64) -> PyResult<f64> {
    let mut total_score = 0.0;
    let hop_count = edge_weights.len() as i32;
    
    for weight in edge_weights {
        total_score += weight;
    }
    
    let finalized_score = total_score * decay_factor.powi(hop_count);
    Ok(finalized_score)
}

/// Ranks a list of nodes based on a base score and relationship connection count.
#[pyfunction]
fn rank_nodes(nodes: Vec<(String, f64)>, connections: Vec<u32>) -> PyResult<Vec<(String, f64)>> {
    let mut ranked = nodes.into_iter().enumerate().map(|(i, (id, base_score))| {
        let conn_count = connections.get(i).cloned().unwrap_or(0);
        let final_score = base_score * (1.0 + (conn_count as f64 * 0.1));
        (id, final_score)
    }).collect::<Vec<_>>();
    
    ranked.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    Ok(ranked)
}

/// A Python module implemented in Rust.
#[pymodule]
fn semantic_brain_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(score_relationship_path, m)?)?;
    m.add_function(wrap_pyfunction!(rank_nodes, m)?)?;
    Ok(())
}
