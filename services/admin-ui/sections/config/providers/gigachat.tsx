import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { PasswordInput } from "@/components/ui/password-input";
import { UseFormReturn } from "react-hook-form";
import { ModelForm } from "./shared";

export const GigaChatForm = ({
  form,
  defaultValues,
}: {
  form: UseFormReturn;
  defaultValues: any;
}) => {
  const supportingModels = ["GigaChat", "GigaChat-Plus", "GigaChat-Pro"];

  return (
    <>
      <FormField
        control={form.control}
        name="gigachat_client_id"
        render={({ field }) => (
          <FormItem>
            <FormLabel>GigaChat Client ID (*)</FormLabel>
            <FormControl>
              <PasswordInput
                placeholder={defaultValues.gigachat_client_id ?? "..."}
                showCopy
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="gigachat_client_secret"
        render={({ field }) => (
          <FormItem>
            <FormLabel>GigaChat Client Secret (*)</FormLabel>
            <FormControl>
              <PasswordInput
                placeholder={defaultValues.gigachat_client_secret ?? "..."}
                showCopy
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <ModelForm
        form={form}
        defaultValues={defaultValues}
        supportedModels={supportingModels}
      />
    </>
  );
};
