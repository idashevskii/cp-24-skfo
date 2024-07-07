import { z } from "zod";
import { BaseConfigSchema } from "./base";

export const YandexGPTConfigSchema = BaseConfigSchema.extend({
  model_provider: z.literal("yandexgpt"),
  yandexgpt_folder_id: z
    .string()
    .nullable()
    .optional()
    .refine(
      (value) => value && value.trim() !== "",
      "YandexGPT Folder ID is requred",
    ),
  yandexgpt_iam_token: z
    .string()
    .nullable()
    .optional()
    .refine(
      (value) => value && value.trim() !== "",
      "YandexGPT IAM Token is requred",
    ),
});

export const DEFAULT_YANDEXGPT_CONFIG: z.input<typeof YandexGPTConfigSchema> = {
  model_provider: "yandexgpt",
  model: "YandexGPT Lite",
  embedding_model: "general:embedding",
  embedding_dim: 1536,
  yandexgpt_folder_id: "",
  yandexgpt_iam_token: "",
};
