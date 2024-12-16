package com.droid.cryptor;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.droid.cryptor.databinding.FragmentEncryptBinding;
import com.droid.cryptor.databinding.FragmentWelcomeBinding;


public class EncryptFragment extends Fragment {

    private FragmentEncryptBinding binding;

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentEncryptBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);


        binding.encrypt.setOnClickListener(v -> {

            if (binding.input.getText().toString().isEmpty()) {
                binding.input.setError("Please enter some data");
                return;
            }
                Bundle bundle = new Bundle();
            bundle.putString("data", binding.input.getText().toString());

            NavHostFragment.findNavController(this)
                            .navigate(R.id.action_EncryptFragment_to_EncryptedFragment, bundle);
                }
        );

    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}