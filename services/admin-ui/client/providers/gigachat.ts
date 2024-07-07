import { z } from "zod";
import { BaseConfigSchema } from "./base";

export const GigaChatConfigSchema = BaseConfigSchema.extend({
  model_provider: z.literal("gigachat"),
  gigachat_client_id: z
    .string()
    .nullable()
    .optional()
    .refine(
      (value) => value && value.trim() !== "",
      "GigaChat Client ID is requred",
    ),
  gigachat_client_secret: z
    .string()
    .nullable()
    .optional()
    .refine(
      (value) => value && value.trim() !== "",
      "GigaChat Client Secret is requred",
    ),
});

export const DEFAULT_GIGACHAT_CONFIG: z.input<typeof GigaChatConfigSchema> = {
  model_provider: "gigachat",
  model: "GigaChat",
  embedding_model: "Embeddings",
  embedding_dim: 1536,
  gigachat_client_id: "",
  gigachat_client_secret: "",
};
