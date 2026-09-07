suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1L) {
  stop("Usage: Rscript scripts/export_appendix_visualizations.R <FELICS faithfulness_results> [thesis data directory]")
}

felics_results <- normalizePath(args[[1L]], mustWork = TRUE)
thesis_data <- if (length(args) >= 2L) args[[2L]] else "data"

specifications <- tibble::tribble(
  ~dataset,             ~model,                 ~n_max,
  "bbq",                "gpt-oss:120b",          4L,
  "bbq",                "mistral-medium-3_5",    4L,
  "medqa",              "gpt-oss:120b",          4L,
  "medqa",              "mistral-medium-3_5",    4L,
  "new_german_credit",  "gpt-oss:120b",          3L,
  "new_german_credit",  "mistral-medium-3_5",    3L
)

file_stem <- function(dataset, model) paste0(
  dataset, "_",
  if (model == "gpt-oss:120b") "gptoss" else "mistral"
)

load_shapley_results <- function(dataset, model, n_max) {
  path <- file.path(
    felics_results,
    dataset,
    paste0(model, "_", n_max),
    paste0(model, "_shapley_ce_estimates.csv")
  )
  read_csv(path, show_col_types = FALSE)
}

question_directory <- file.path(thesis_data, "appendix", "ce_shift_identity")
normalization_directory <- file.path(thesis_data, "appendix", "rq3_normalization_identity")
credit_directory <- file.path(thesis_data, "appendix", "rq3_credit_concept_delta")
dir.create(question_directory, recursive = TRUE, showWarnings = FALSE)
dir.create(normalization_directory, recursive = TRUE, showWarnings = FALSE)
dir.create(credit_directory, recursive = TRUE, showWarnings = FALSE)

credit_concept_order <- c(
  "Credit Purpose",
  "Credit Amount",
  "Credit Term (Months)",
  "Liquid Assets",
  "Household Income",
  "SCHUFA Score (%)",
  "Real Estate Value",
  "Applicant Age",
  "Lives In Own House",
  "Current Monthly Debt Burden",
  "Job Category",
  "Household Size"
)

for (index in seq_len(nrow(specifications))) {
  specification <- specifications[index, ]
  data <- load_shapley_results(
    specification$dataset,
    specification$model,
    specification$n_max
  ) %>%
    filter(
      is.finite(atomic_kl_div),
      is.finite(shapley_kl_div),
      is.finite(adjusted_shapley_kl_div)
    )

  stem <- file_stem(specification$dataset, specification$model)

  question_data <- data %>%
    group_by(example_idx) %>%
    summarise(
      concept_count = n(),
      atomic_ce = mean(atomic_kl_div),
      interaction_ce = mean(adjusted_shapley_kl_div),
      .groups = "drop"
    ) %>%
    mutate(marker_size = 0.65 + 0.35 * sqrt(concept_count)) %>%
    arrange(example_idx)

  write_csv(
    question_data,
    file.path(question_directory, paste0(stem, ".csv"))
  )

  normalization_data <- data %>%
    group_by(example_idx) %>%
    mutate(concept_index = row_number()) %>%
    ungroup() %>%
    transmute(
      observation_id = row_number(),
      example_idx = as.integer(example_idx),
      concept_index = as.integer(concept_index),
      raw_ce = shapley_kl_div,
      adjusted_ce = adjusted_shapley_kl_div
    )

  write_csv(
    normalization_data,
    file.path(normalization_directory, paste0(stem, ".csv"))
  )

  if (specification$dataset == "new_german_credit") {
    credit_data <- data %>%
      mutate(concept_id = match(intrv_concepts, credit_concept_order)) %>%
      group_by(concept_id) %>%
      summarise(
        n_questions = n(),
        mean_raw_ce = mean(shapley_kl_div),
        mean_adjusted_ce = mean(adjusted_shapley_kl_div),
        mean_delta_ce = mean(adjusted_shapley_kl_div - shapley_kl_div),
        .groups = "drop"
      ) %>%
      arrange(concept_id)

    if (anyNA(credit_data$concept_id) || nrow(credit_data) != length(credit_concept_order)) {
      stop("Unexpected New German Credit concept labels in ", stem)
    }

    write_csv(
      credit_data,
      file.path(credit_directory, paste0(stem, ".csv"))
    )
  }
}

cat("Exported appendix visualization data to ", normalizePath(thesis_data), "\n", sep = "")
