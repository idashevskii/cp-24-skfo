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

export const YandexGPTForm = ({
  form,
  defaultValues,
}: {
  form: UseFormReturn;
  defaultValues: any;
}) => {
  const supportingModels = [
    "YandexGPT Pro",
    "YandexGPT Lite",
    "YandexGPT Lite RC",
    "Summary"
  ];

  return (
    <>
      <FormField
        control={form.control}
        name="yandexgpt_folder_id"
        render={({ field }) => (
          <FormItem>
            <FormLabel>YandexGPT Folder ID (*)</FormLabel>
            <FormControl>
              <PasswordInput
                placeholder={defaultValues.yandexgpt_folder_id ?? "..."}
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
        name="yandexgpt_iam_token"
        render={({ field }) => (
          <FormItem>
            <FormLabel>YandexGPT IAM Token (*)</FormLabel>
            <FormControl>
              <PasswordInput
                placeholder={defaultValues.yandexgpt_iam_token ?? "t1.9eu"}
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
